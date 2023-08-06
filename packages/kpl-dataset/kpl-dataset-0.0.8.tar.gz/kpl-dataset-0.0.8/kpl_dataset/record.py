import kpl_dataset.define_pb2 as define
import os
import shutil
import uuid


class BasicType:
    String = "String"
    Int = "Int"
    Float = "Float"
    ByteArray = "ByteArray"
    File = "File"


class FileType:
    Small = 0
    Large = 1


_SIZE_THRESHOLD = 50 * (1 << 20)  # 50MB
_FILE_ROOT = "files"


def set_size_threshold(size):
    global _SIZE_THRESHOLD
    _SIZE_THRESHOLD = size


class RecordDefine:
    ROOT = None

    @staticmethod
    def encode_map(value, proto, record_type):
        map_protobuf = proto.map
        for k, v in value.items():
            assert isinstance(k, str)
            if isinstance(v, (list, tuple)):
                feature = define.Feature()
                RecordDefine.encode_list(v, feature.feature_list_field, record_type[k])
                map_protobuf[k].CopyFrom(feature)
            elif isinstance(v, dict):
                feature = define.Feature()
                RecordDefine.encode_map(v, feature.feature_map_field, record_type[k])
                map_protobuf[k].CopyFrom(feature)
            else:
                feature = define.Feature()
                RecordDefine.encode_basic(v, feature, record_type[k])
                map_protobuf[k].CopyFrom(feature)

    @staticmethod
    def encode_basic(value, proto, record_type):
        if record_type == BasicType.Int:
            proto.int64_field = value
        elif record_type == BasicType.ByteArray:
            proto.bytes_field = value
        elif record_type == BasicType.String:
            proto.bytes_field = value.encode()
        elif record_type == BasicType.Float:
            proto.float64_field = value
        elif record_type == BasicType.File:
            file = define.FileContent()
            size = os.path.getsize(value)
            file.size = size
            if size > _SIZE_THRESHOLD:
                with open(value, "rb") as fi:
                    file.type = define.FileContent.FileType.large
                    file.bytes_field = fi.read(512)
                rel_path = "{}/{}".format(_FILE_ROOT, uuid.uuid1().hex)
                target_path = "{}/{}".format(RecordDefine.ROOT, rel_path)
                file.file_path = rel_path
                shutil.copyfile(value, target_path)
            else:
                with open(value, "rb") as fi:
                    file.type = define.FileContent.FileType.small
                    file.bytes_field = fi.read()
                file.file_path = ""
            proto.file_field.CopyFrom(file)
        else:
            raise Exception("Type `{}` not supported".format(record_type))

    @staticmethod
    def encode_list(value, proto, record_type):
        for i, v in enumerate(value):
            feature = proto.list.add()
            if isinstance(v, (list, tuple)):
                RecordDefine.encode_list(v, feature.feature_list_field, record_type[0])
            elif isinstance(v, dict):
                RecordDefine.encode_map(v, feature.feature_map_field, record_type[0])
            else:
                RecordDefine.encode_basic(v, feature, record_type[0])

    @staticmethod
    def decode_basic(feature, record_type):
        if record_type == BasicType.Int:
            return feature.int64_field
        elif record_type == BasicType.ByteArray:
            return feature.bytes_field
        elif record_type == BasicType.Float:
            return feature.float64_field
        elif record_type == BasicType.String:
            # 中文可能decode错误
            try:
                return feature.bytes_field.decode()
            except:
                return feature.bytes_field.decode("GBK")
        elif record_type == BasicType.File:
            return {
                "type": feature.file_field.type,
                "content": feature.file_field.bytes_field,
                "file_path": feature.file_field.file_path,
                "size": feature.file_field.size,
            }
        else:
            raise Exception("Type `{}` not supported".format(record_type))

    @staticmethod
    def decode_map(feature, record_type):
        f_map = feature.map
        ret = {}
        for k, v in record_type.items():
            if isinstance(v, list):
                ret[k] = RecordDefine.decode_list(f_map[k].feature_list_field, v)
            elif isinstance(v, dict):
                ret[k] = RecordDefine.decode_map(f_map[k].feature_map_field, v)
            else:
                ret[k] = RecordDefine.decode_basic(f_map[k], v)
        return ret

    @staticmethod
    def decode_list(feature, record_type):
        f_list = feature.list
        ret = []
        v = record_type[0]
        if isinstance(v, list):
            for i in range(len(f_list)):
                ret.append(RecordDefine.decode_list(f_list[i].feature_list_field, v))
        elif isinstance(v, dict):
            for i in range(len(f_list)):
                ret.append(RecordDefine.decode_map(f_list[i].feature_map_field, v))
        else:
            for i in range(len(f_list)):
                ret.append(RecordDefine.decode_basic(f_list[i], v))
        return ret

    @staticmethod
    def encode(value, record_type):
        feature = define.FeatureMap()
        RecordDefine.encode_map(value, feature, record_type)
        return feature

    @staticmethod
    def decode(feature, record_type):
        return RecordDefine.decode_map(feature, record_type)

    @staticmethod
    def encode_meta(record_type, id, version):
        meta = define.Meta()
        meta.version = version
        meta.id = id
        meta.record_type.CopyFrom(RecordDefine._encode_meta(record_type))
        return meta

    @staticmethod
    def _encode_meta(record_type):
        rt = define.RecordType()
        if isinstance(record_type, dict):
            assert len(record_type) > 0, "[RecordType] dict cannot be empty"
            rt.basicType = define.RecordType.BasicType.map
            properties = rt.properties
            for k, v in record_type.items():
                assert isinstance(k, str), "[RecordType] key must be string. but get {}: {}".format(k, type(k))
                rt.keys.append(k)
                properties[k].CopyFrom(RecordDefine._encode_meta(v))
        elif isinstance(record_type, list):
            assert len(record_type) == 1, "[RecordType] list length must equals 1. but get {}".format(record_type)
            rt.basicType = define.RecordType.BasicType.list
            rt.item.CopyFrom(RecordDefine._encode_meta(record_type[0]))
        elif record_type == BasicType.ByteArray:
            rt.basicType = define.RecordType.BasicType.bytes
        elif record_type == BasicType.Float:
            rt.basicType = define.RecordType.BasicType.float64
        elif record_type == BasicType.Int:
            rt.basicType = define.RecordType.BasicType.int64
        elif record_type == BasicType.String:
            rt.basicType = define.RecordType.BasicType.string
        elif record_type == BasicType.File:
            rt.basicType = define.RecordType.BasicType.file
        else:
            raise Exception("BasicType {} is not supported".format(record_type))
        return rt

    @staticmethod
    def decode_meta(meta):
        if meta.basicType == define.RecordType.BasicType.string:
            return BasicType.String
        elif meta.basicType == define.RecordType.BasicType.int64:
            return BasicType.Int
        elif meta.basicType == define.RecordType.BasicType.bytes:
            return BasicType.ByteArray
        elif meta.basicType == define.RecordType.BasicType.float64:
            return BasicType.Float
        elif meta.basicType == define.RecordType.BasicType.file:
            return BasicType.File
        elif meta.basicType == define.RecordType.BasicType.list:
            return [RecordDefine.decode_meta(meta.item)]
        elif meta.basicType == define.RecordType.BasicType.map:
            ret = {}
            for k, p in meta.properties.items():
                ret[k] = RecordDefine.decode_meta(p)
            return ret
        else:
            raise Exception("Unknown type {}".format(meta.basicType))


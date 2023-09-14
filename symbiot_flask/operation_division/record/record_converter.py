from .step_record import StepRecord
from .script_record import ScriptRecord
from .record_entity import RecordEntity


def type_to_string(record):
    if type(record) is RecordEntity:
        return "entity"
    elif type(record) is StepRecord:
        return "step"
    elif type(record) is ScriptRecord:
        return "script"
    else:
        raise ValueError("Unsupported container type")


def from_entity(entity):
    inputs = [bridge_read(input_) for input_ in entity.inputs]
    outputs = None if entity.outputs is None else \
        [bridge_read(output_) for output_ in entity.outputs]

    args = entity.__dict__.copy()
    args.pop("inputs")
    args.pop("outputs")

    if entity.type_ == "step":
        return StepRecord(
            inputs,
            outputs=outputs,
            id_=entity.id,
            **args)
    elif entity.type_ == "script":
        return ScriptRecord(
            inputs,
            outputs=outputs,
            id_=entity.id,
            **args)


def to_entity(record) -> RecordEntity:
    type_ = type_to_string(record)

    if type_ == "entity":
        return record

    args = record.__dict__.copy()
    args.pop("inputs")
    args.pop("outputs")

    return RecordEntity(
        type_,
        inputs=[bridge_format(bridge) for bridge in record.inputs],
        outputs=[bridge_format(bridge) for bridge in record.outputs],
        **args
    )


"""
        1<b>list<b>
          str<l1>dupa<el1>
          int<l1>1

        2<b>list<b>
          list<l1>
              str<l2>pyra<el2>
              int<l2>3<el1>
          list<l1>
              str<l2>dupa<el2>
              int<l2>52
        """


def bridge_format(data):
    def type_format(d):
        return str(type(d)) \
            .replace('<class ', '') \
            .replace("'", "") \
            .replace('>', '')

    def format_(d, lev):
        if isinstance(d, (str, int, bool, float)):
            return f"{type_format(d)}<@level{lev}>{str(d)}"
        elif isinstance(d, list):
            res = f"<@el{lev}>".join(
                [format_(x, lev+1)
                 for x in d])
            return f"{type_format(d)}<@level{lev}>{res}"
            # TODO: add support for set and dict
        raise NotImplementedError("Not implemented data type")

    return format_(data, 0)


def bridge_read(bridge):
    def read(b, lev):
        print(f"lev: {lev}")
        t, d = b.split(f"<@level{lev}>")
        match t:
            case "str": return d
            case "int": return int(d)
            case "bool": return bool(d)
            case "float": return float(d)
            case "list":
                res = [read(el, lev+1)
                       for el in d.split(f"<@el{lev}>")]
                return res
            # TODO: add support for set and dict

    return read(bridge, 0)
from schema import Schema, And


options_schema = Schema(
    {
        'minutes': And(int, lambda x: x > 0),
    },
    ignore_extra_keys=True,
)

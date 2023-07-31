from voluptuous import Any, Optional, Schema

FEELS_LIKE_RANK_SCHEMA = Schema(
    schema={
        Optional('order_dir'): Any('desc', 'asc'),
    },
)

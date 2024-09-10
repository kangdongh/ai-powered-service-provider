def example_service_1(arg1, arg2):
    return f"Processed {arg1} and {arg2}"

service_info_1 = {
    "description": "This service processes two random arguments and returns a combined string.",
    "kwargs": {
        "arg1": {
            "description": "The first argument to process",
            "type": str
        },
        "arg2": {
            "description": "The second argument to process",
            "type": str
        }
    },
    "return_type": str
}

def example_service_2(arg1, arg2):
    return f"Here is a joke with {arg1} and {arg2}"

service_info_2 = {
    "description": "This service provides random joke based on your query.",
    "kwargs": {
        "arg1": {
            "description": "The first single word for joke",
            "type": str
        },
        "arg2": {
            "description": "The second single word for joke",
            "type": str
        }
    },
    "return_type": str
}
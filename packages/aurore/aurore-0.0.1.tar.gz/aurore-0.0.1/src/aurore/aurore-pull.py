import json

def add_args(parser):
    parser.add_argument("filename")

def init(args,accum):
    with open(args.filename,"r") as f:
        accum.update({"pull": {
            "source-data": json.load(f) 
            }
        })
    pass 

def item():
    pass

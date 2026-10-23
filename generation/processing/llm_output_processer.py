import json
from pathlib import Path
import jinja2
from rdflib import URIRef


environment = jinja2.Environment(loader=jinja2.FileSystemLoader(["./generation/processing"]))

def uri(value):
    return isinstance(value, URIRef)

environment.tests['uri'] = uri


def render_feature_shape(shape_name, base_shape, subshapes=[]):
    feature_shape_template = environment.get_template('feature_shape.ttl.jinja')
    feature_shape = feature_shape_template.render(shape_name = shape_name, base_shape = base_shape, subshapes = subshapes)
    return feature_shape
    
def render_label_shape(shape_name, base_shape, subshapes=[]):
    feature_shape_template = environment.get_template('label_shape.ttl.jinja')
    feature_shape = feature_shape_template.render(shape_name = shape_name, base_shape = base_shape, subshapes = subshapes)
    return feature_shape

def render_dataset_shape(shape_name, base_shape, subshapes=[]):
    feature_shape_template = environment.get_template('dataset_shape.ttl.jinja')
    feature_shape = feature_shape_template.render(shape_name = shape_name, base_shape = base_shape, subshapes = subshapes)
    return feature_shape

def render_model_shape(shape_name, target):
    feature_shape_template = environment.get_template('model_shape.ttl.jinja')
    feature_shape = feature_shape_template.render(shape_name = shape_name, target = target)
    return feature_shape

def render_transformation(insertions, dependences, conditions, columnar_type = True):
    if len(insertions) <= 0:
        return None
    
    transf_template = environment.get_template("transformation_query.sparql.jinja")
    transf = transf_template.render(insertions = insertions, dependences = dependences, conditions = conditions, columnarType = columnar_type)
    return transf


def open_file(file_path:Path):
    with open(file_path, mode='r') as f:
        file = f.read()
    return file


def render_shapes_from_io(io_port, spec_path):

    dependences = set()
    transformations = set()
    for feature in io_port["feature_properties"]:
        if feature.find('cb:') != -1:
            feature = feature[3:]

        feature_name = f"{feature}FeatureShape"

        print("feature", feature)
        rendered_shape = render_feature_shape(feature_name, feature)
        print("Guardant", spec_path /f"{feature_name}.ttl")
        with open( spec_path /f"{feature_name}.ttl", mode='w') as f:
            f.write(rendered_shape)

    dependences = set()
    transformations = set()
    for label in io_port["label_properties"]:
        if label.find('cb:') != -1:
            label = label[3:]
        print("label", label)
        label_name = f"{label}LabelShape" 
        rendered_shape = render_label_shape(f"{label_name}", label)
        with open( spec_path /f"{label_name}.ttl", mode='w') as f:
            f.write(rendered_shape)
            
    for data in io_port["dataset_properties"]:
        if data.find('cb:') != -1:
            data = data[3:]
        print("data",data)
        data_name = f"{data}DatasetShape"
        rendered_shape = render_dataset_shape(data_name, data)
        with open( spec_path /f"{data_name}.ttl", mode='w') as f:
            f.write(rendered_shape)
    
    

def process_llm_output(sklearn_components:dict, llm_output='./llm_output/', dest='./processing/clean'):
    gpt = Path(llm_output)
    gpt_out = Path(dest)


    for component in sklearn_components.values():
        print(f"####################### {component['name']} ###########################")

        if not component["needs_parameter_specification"] and component['name'] not in ['MissingIndicator']:
            component_path:Path = gpt / f"{component['name']}.json"
            component_out = gpt_out / component["name"]
            component_out.mkdir(exist_ok=True)
            component_inputs = component_out / "input"
            component_inputs.mkdir(exist_ok=True)
            component_outputs = component_out / "output"
            component_outputs.mkdir(exist_ok=True)

            with open(component_path) as f:
                component_json = json.load(f)[component["name"]]
            

            for num,i in enumerate(component_json["inputs"]):
                spec_path = component_inputs / f"{num}"
                spec_path.mkdir(exist_ok=True)
                render_shapes_from_io(i, spec_path)

            if component["estimator_type"] == "transformer":
                print(component_json["data_outputs"])
                
                for num, o in enumerate(component_json["data_outputs"]):
                    spec_path = component_outputs / f"{num}"
                    spec_path.mkdir(exist_ok=True)
                    render_shapes_from_io(o, spec_path)

            else:
                print("No data outputs")  
                num = 0

            if "model_output" in component_json and component["estimator_type"] not in ["cluster"]: 

                if component_json["model_output"] == {}: 
                    model = "TransformerModel"
                else:
                    model = component_json["model_output"]["model_type"]

                print("model", model)

                spec_path = component_outputs / f"{len(component_json['data_outputs'])}"
                spec_path.mkdir(exist_ok=True)
                rendered_shape = render_model_shape(f"{model}ModelShape", model)
                with open( spec_path /f"{model}ModelShape.ttl", mode='w') as f:
                    f.write(rendered_shape)

                    
        else:
            print("Component no materialitzat per paràmetre obligatori")

def main():
    with open("./sklearn/sklearn_miner.json") as f:
        raw = f.read()

    sklearn_components = json.loads(raw)
    process_llm_output(sklearn_components)


if __name__ == '__main__':
    main()
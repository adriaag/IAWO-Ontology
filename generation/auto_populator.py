from ontology_generation import tbox_generator, abox_generator
from sklearn_api_miner import sklearn_miner
from processing import llm_output_processer
import json



# Sklearn API query
sklearn_path = './generation/sklearn_api_miner/sklearn_miner.json'
sklearn_miner.mine(dest= sklearn_path)
with open(sklearn_path) as f:
    raw = f.read()
    sklearn_components = json.loads(raw)


# Processing of LLM output
clean_shapes_path = './generation/processing/clean'
llm_output_processer.process_llm_output(sklearn_components=sklearn_components,
                                        llm_output='./generation/llm_output',
                                        dest= clean_shapes_path)


# Ontology generation
tbox_generator.main(dest = 'TBOX.ttl')
abox_generator.main(sklearn_components=sklearn_components,
                    dataCharactheristicsPath='./generation/ontology_generation/dataCharactheristics.ttl',
                    sahpesPath=clean_shapes_path,
                    dest= 'ABOX.ttl')


"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import handle_missing_data, one_hot_encoding, binning, feature_scaling, feature_creation

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=handle_missing_data,
                inputs="raw_credit_card_txns",
                outputs="int_credit_card_txns_missing_data_handled",
                name="handle_missing_data_node",
            ),
            node(
                func=one_hot_encoding,
                inputs="int_credit_card_txns_missing_data_handled",
                outputs="int_credit_card_txns_one_hot_encoded",
                name="one_hot_encoding_node",
            ),
            node(
                func=binning,
                inputs="int_credit_card_txns_one_hot_encoded",
                outputs="int_credit_card_txns_binned",
                name="binning_node",
            ),
            node(
                func=feature_scaling,
                inputs="int_credit_card_txns_binned",
                outputs="int_credit_card_txns_feature_scaled",
                name="feature_scaling_node",
            ),
            node(
                func=feature_creation,
                inputs="int_credit_card_txns_feature_scaled",
                outputs="feature_credit_card_txns",
                name="feature_creation_node",
            ),
        ]
    )


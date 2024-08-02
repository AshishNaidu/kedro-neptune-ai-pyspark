"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.6
"""
import pyspark.sql.functions as F
from pyspark.ml.feature import StringIndexer, OneHotEncoder, Bucketizer, StandardScaler, VectorAssembler
from pyspark.ml import Pipeline

def handle_missing_data(df):
    for column in df.columns:
        if df.select(column).dtypes[0][1] in ["int", "double"]:
            mean_value = df.select(F.mean(F.col(column))).collect()[0][0]
            df = df.fillna(mean_value, subset=[column])
    return df

def one_hot_encoding(df):
    input_col = "TX_FRAUD_SCENARIO"
    output_col = "TX_FRAUD_SCENARIO_VEC"
    indexer = StringIndexer(inputCol=input_col, outputCol=f"{input_col}_index")
    encoder = OneHotEncoder(inputCol=f"{input_col}_index", outputCol=output_col)
    pipeline = Pipeline(stages=[indexer, encoder])
    df = pipeline.fit(df).transform(df)
    return df

def binning(df):
    input_col = "TX_AMOUNT"
    output_col = "TX_AMOUNT_BINNED"
    splits = [-float("inf"), 10, 50, 100, float("inf")]
    bucketizer = Bucketizer(splits=splits, inputCol=input_col, outputCol=output_col)
    df = bucketizer.transform(df)
    return df

def vectorize_column(df, input_col, output_col):
    assembler = VectorAssembler(inputCols=[input_col], outputCol=output_col)
    df = assembler.transform(df)
    return df

def feature_scaling(df):
    input_col = "TX_AMOUNT"
    output_col = "TX_AMOUNT_SCALED"
    vector_col = f"{input_col}_vec"
    df = vectorize_column(df, input_col, vector_col)
    scaler = StandardScaler(inputCol=vector_col, outputCol=output_col)
    scaler_model = scaler.fit(df)
    df = scaler_model.transform(df)
    return df

def feature_creation(df):
    input_col = "TX_AMOUNT"
    output_col = "HIGH_VALUE_TX"
    threshold = 50
    df = df.withColumn(output_col, F.when(F.col(input_col) > threshold, 1).otherwise(0))
    return df

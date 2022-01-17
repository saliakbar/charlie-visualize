import findspark
findspark.init()
import plotly.express as px
import pyspark.sql.functions as F
from pyspark import SparkContext
from pyspark.sql.session import SparkSession

import utils as u


def get_abstraction_grouping_columns(abstraction: str):
    """
    Gets the columns `packageName`, `className`, and `methodName` depending
    on the `abstraction` level ("package", "class", "method").
    """
    if abstraction == "method":
        return [u.packageName, u.className, u.methodName]
    elif abstraction == "class":
        return [u.packageName, u.className]
    elif abstraction == "package":
        return [u.packageName]


def get_api_grouping_columns(characterization_type: str):
    """
    Gets the columns `api`, `mcrCategories`, and `mcrTags` depending
    on the `characterization_type` ("api", "mcrCategories", "mcrTags").
    """
    if characterization_type == u.api:
        return [characterization_type, u.mcrCategories, u.mcrTags]
    return [u.mcrCategories, u.mcrTags]


def getDependenceString(apply_dependence: bool):
    """
    Returns "_with_dep" if `apply_dependence` is true.
    """
    if apply_dependence:
        return "_with_dep"
    return ""


def characterize_abstractions(repository: str, abstraction: str, characterization_type: str, apply_dependence: bool):
    """
    Characterizes the `abstractions` of the `repository` with the `characterization_type` and the
    dependence relationships if `apply_dependence` is true.
    """
    abstr_group_cols = get_abstraction_grouping_columns(abstraction)
    api_group_cols = abstr_group_cols.copy()
    api_group_cols.extend(
        get_api_grouping_columns(characterization_type))

    #print(u.data_dir)
    df1 = u.read_csv(spark, u.data_dir + repository + ".csv") \
        .select(abstr_group_cols) \
        .fillna(".").distinct()

    df2 = u.read_csv(spark, u.analyzed_data_dir + abstraction + "/" +
                     u.api_proportion_file + abstraction + "_" + repository + ".csv") \
        .fillna(".", abstr_group_cols)

    if characterization_type == u.mcrTags:
        df2 = df2.withColumn(u.mcrTags, F.split(
            F.regexp_replace(u.mcrTags, "[\[\]]", ""), ",")) \
            .withColumn(u.mcrTags, F.explode(u.mcrTags))

    if apply_dependence:
        df = u.read_csv(spark, u.analyzed_data_dir + abstraction + "/" + u.api_sets_file +
                        abstraction + "_" + repository + ".csv") \
            .fillna(".", abstr_group_cols) \
            .withColumn(u.apis, F.split(
                F.regexp_replace(u.apis, "[\[\]]", ""), ",")) \
            .withColumn("dependence1",
                        F.when(F.array_contains(u.apis, dependency1) &
                               F.array_contains(u.apis, dependency5), True).otherwise(False)) \
            .withColumn("dependence2",
                        F.when(F.array_contains(u.apis, dependency2) &
                               F.array_contains(u.apis, dependency5), True).otherwise(False)) \
            .withColumn("dependence3",
                        F.when(F.array_contains(u.apis, dependency3) &
                               F.array_contains(u.apis, dependency4), True).otherwise(False)) \
            .withColumn("dependence4",
                        F.when(F.array_contains(u.apis, dependency4) &
                               F.array_contains(u.apis, dependency6), True).otherwise(False))

        if characterization_type == u.mcrTags:
            df2 = df2.join(df, (df2[u.packageName] == df[u.packageName]) &
                           (df2[u.className] == df[u.className]) &
                           (df2[u.methodName] == df[u.methodName]) &
                           ((df["dependence1"] & df2[u.mcrTags].isin(dependence1tags)) |
                            (df["dependence2"] & df2[u.mcrTags].isin(dependence2tags)) |
                            (df["dependence3"] & df2[u.mcrTags].isin(dependence3tags)) |
                            (df["dependence4"] & df2[u.mcrTags].isin(dependence3tags))), "leftanti")
        else:
            df2 = df2.join(df, (df2[u.packageName] == df[u.packageName]) &
                           (df2[u.className] == df[u.className]) &
                           (df2[u.methodName] == df[u.methodName]) &
                           ((df["dependence1"] & (df2[u.api] == dependency1)) |
                            (df["dependence2"] & (df2[u.api] == dependency2)) |
                            (df["dependence3"] & (df2[u.api] == dependency3))), "leftanti")

    df2 = df2.select(api_group_cols).filter(
        F.col(characterization_type).isNotNull())

    data = df1.join(df2, abstr_group_cols, how="left").fillna("none")

    u.delete_dir(u.spark_dir)
    u.write_csv(data.coalesce(1), u.spark_dir)
    u.copy_csv(u.spark_dir, u.characterization_dir + u.characterization_file +
               repository + "_" + abstraction + "_" + characterization_type + getDependenceString(apply_dependence) + ".csv")


def visualize(repository: str, abstraction: str, characterization_type: str, apply_dependence: bool):
    """
    Visualizes the `repository` using the `abstractions` that were characterized with the
    `characterization_type` and the dependence relationships if `apply_dependence` is true.
    """
    data = u.read_csv(spark, u.characterization_dir + u.characterization_file + repository + "_" +
                      abstraction + "_" + characterization_type + getDependenceString(apply_dependence) + ".csv")
    data = data.toPandas()
    path_cols = get_abstraction_grouping_columns(abstraction)
    path_cols.append(characterization_type)
    fig = px.treemap(
        data, path=path_cols, hover_data=get_api_grouping_columns(characterization_type), color=characterization_type,
        color_discrete_sequence=["burlywood", "mediumaquamarine", "deepskyblue", "yellow",
                                 "lavender", "pink", "#c37c4a", "gold", "sandybrown", "silver", "gray"],
        color_discrete_map={"(?)": "#ffd695", "none": "#66b35d", "junit:junit": "#4c8ed4", "Testing Frameworks": "#4c8ed4", "testing": "#4c8ed4",
                            "org.mockito:mockito-core": "#e45756", "Mocking": "#e45756", "mock": "#e45756",
                            "org.hamcrest:hamcrest-all": "greenyellow", "matching": "greenyellow",
                            "org.apache.lucene:lucene-core": "orchid", "Full-Text Indexing Libraries": "orchid", "lucene": "orchid",
                            "org.apache.lucene:lucene-analyzers-common": "aqua"})
    fig.write_html(u.visualization_dir + u.visualization_file + repository + "_" + abstraction +
                   "_" + characterization_type + getDependenceString(apply_dependence) + ".html", auto_open=True)
    fig.write_image(u.visualization_dir + u.visualization_file + repository + "_" + abstraction +
                    "_" + characterization_type + getDependenceString(apply_dependence) + ".pdf", width=1500, height=1000)


if __name__ == "__main__":
    #print('Hello')
    sc = SparkContext("local", "applying-apis")
    spark = SparkSession(sc)

    dependency1 = "org.mockito:mockito-core"
    dependency2 = "org.hamcrest:hamcrest-all"
    dependency3 = "org.apache.lucene:lucene-analyzers-common"
    dependency4 = "org.apache.lucene:lucene-core"
    dependency5 = "junit:junit"
    dependency6 = "org.apache.lucene:lucene-analyzers-smartcn"

    dependence1tags = ["mock", "mocking", "junit"]
    dependence2tags = ["matching", "junit"]
    dependence3tags = ["analyzer", "indexing", "full-text"]

    repositories = [
        "Novetta/CLAVIN"
    ]

    for repository in repositories:
        repository = repository.replace("/", "_")
        characterize_abstractions(repository, "method", u.api, False)
        visualize(repository, "method", u.api, False)
        characterize_abstractions(repository, "method", u.mcrCategories, False)
        visualize(repository, "method", u.mcrCategories, False)
        characterize_abstractions(repository, "method", u.mcrCategories, True)
        visualize(repository, "method", u.mcrCategories, True)
        characterize_abstractions(repository, "method", u.mcrTags, False)
        visualize(repository, "method", u.mcrTags, False)
        characterize_abstractions(repository, "method", u.mcrTags, True)
        visualize(repository, "method", u.mcrTags, True)

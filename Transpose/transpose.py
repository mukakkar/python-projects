from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, concat_ws, lit, split, udf
from pyspark.sql.types import StringType


def generate_transpose_file(input_file, output_dir, spark):
    """ function to generate the Transpose file
      input_file = input csv file
      output_dir = directory to generate output
      spark = spark session object

     transpose file is transpose of entities in the input file i.e
                  entity  attr1     attr2   attr3 ......... timestamp
     input_row = e1         v1      v2      v3    .........  t

     output = entity  attribute   value    timestamp
                e1     attr1      v1       t
                e1     attr2      v2       t
                e1     attr3      v3       t
                .       .          .       .
                .       .          .       .
                .       .          .       .
                .       .          .       .
                e1     attrn      vn       t
    """
    def merge_av(attributes,values):
        """
        function to merge attribute value and generate a,v pairs sepearted by string -

        :param attributes:
        :param values:
        :return:
        """
        return '-'.join([ attribute + ',' + value
                          for attribute, value in
                          zip(attributes.split(','), values.split(','))])

    # 1.generate the master dataframe , schema isn't required so skipping schema parameter
    inputdf = spark.read.csv(input_file, header=True)

    # 2.get the columns i.e entity, attr1 , attr2 ..... attrn , timestamp
    columns = inputdf.columns

    # 3.create a new dataframe with schema entity timestamp value attribute
    #   entity      timestamp      value                        attribute
    #    e1             t1         e1_v1,e1_v2,e1_v3....e1_vn   a1,a2,a3,.....an
    #    e2             t2         e2_v1,e2_v2,e2_v3....e2_vn   a1,a2,a3,.....an
    #    e3             t3         e3_v1,e3_v2,e3_v3....e3_vn   a1,a2,a3,.....an
    #    e4             t4         e4_v1,e4_v2,e4_v3....e4_vn   a1,a2,a3,.....an
    #    e5             t5         e5_v1,e5_v2,e5_v3....e5_vn   a1,a2,a3,.....an
    #    .......................................................................
    #    .......................................................................
    #    e3             tn         en_v1,en_v2,en_v3....en_vn   a1,a2,a3,.....an
    transpose_initdf = inputdf.select(columns[0], columns[-1],
                                 concat_ws(',',*columns[1:-1]).alias('value'))\
        .withColumn('attribute', lit(','.join(columns[1:-1])))

    udf_mergeav = udf(merge_av, StringType())

    # 4.create a new dataframe witj schema entity timestamp av
    #   entity      timestamp      av
    #    e1             t1         a1,e1_v1-a2,e1_v2-a3,e1_v3....-an,e1_vn
    #    e2             t2         a1,e2_v1-a2,e2_v2-a3,e2_v3....-an,e2_vn
    #    e3             t3         a1,e3_v1-a2,e3_v2-a3,e3_v3....-an,e3_vn
    #    e4             t4         a1,e4_v1-a2,e4_v2-a3,e4_v3....-an,e4_vn
    #    e5             t5         a1,e5_v1-a2,e5_v2-a3,e5_v3....-an,e5_vn
    #    e6             t6         a1,e6_v1-a2,e6_v2-a3,e6_v3....-an,e6_vn
    #    .......................................................................
    #    .......................................................................
    #    en             tn         a1,en_v1-a2,en_v2-a3,en_v3....-an,en_vn

    transpose_merged_df = transpose_initdf.select(columns[0], columns[-1],
                                      udf_mergeav('attribute','value').alias('av'))

    # 5.create a new dataframe witj schema entity atribute value timestamp
    # first use explode convert each row in to multiple row i.e using - as splitter
    # i.e e1             t1         a1,e1_v1-a2,e1_v2-a3,e1_v3....-an,e1_vn transfroms to
    # e1  t1  a1,e1_a1
    # e1  t1  a2,e1_a2
    # ...
    # e1  t1  an,e1_an
    # then split column av in to column attribute & value
    # The final schema should be as follows
    # ClientID	Attribute	Value		timestamp
    #     e1   		a1      e1_v1		t1
    #     e1   		a2      e1_v2		t1
    #     e1   		a3      e1_v3		t1
    #     .............................
    #     e1   		an      e1_vn		t2
    #     e2   		a1      e2_v1		t2
    #     e2   		a2      e2_v2		t2
    #     e2   		a3      e2_v3		t2
    #     .............................
    #     e2   		an      e2_vn		t2
    #     .............................
    #     .............................
    #     en   		an-1    en_vn-1	tn
    #     en   		an      en_vn		tn

    transpose_finaldf = transpose_merged_df.select( \
            columns[0], columns[-1], explode(split('av','-')).alias('av')). \
            select(columns[0],
                    split('av',',').getItem(0).alias('attribute'),
                    split('av',',').getItem(1).alias('value'),
                    columns[-1])

    # by default spark uses 200 partitions which is inefficient for small daat sets
    # setting it to 6 to generate 6 output files
    spark.conf.set("spark.sql.shuffle.partitions", 6)
    transpose_finaldf.write.csv(output_dir)

if __name__ == "__main__":

    from sys import argv
    spark = SparkSession \
        .builder \
        .appName("Transpose") \
        .getOrCreate()

    try:
        generate_transpose_file(argv[1], argv[2], spark)
    except Exception as e:
        print 'Error while running spark job , the error is {error}'.format(error = repr(e))
    finally:
        spark.stop()


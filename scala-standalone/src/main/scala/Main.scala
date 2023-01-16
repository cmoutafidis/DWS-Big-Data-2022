package main.scala

import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.storage.StorageLevel

import scala.collection.mutable.ListBuffer
import scala.io.Source

object Main {
  case class Point(id: Int, values: List[Double], sum: Double)

  def readCsv(filename: String): RDD[Point] = {
    val records = new ListBuffer[Point]()
    val source = Source.fromFile(filename)
    var l = 0
    for (line <- source.getLines()) {
      if (l != 0) {
        val d = line.trim.split(",") //split with ,
        val values = d.tail.map(_.toDouble).toList // except for the first element the others refer to values
        records += Point(d.head.toInt, values, values.sum) //create a record
      }
      l += 1
    }
    source.close()

    SparkSession.builder().getOrCreate()
      .sparkContext.parallelize(
      records.toList.sortWith((x, y) => x.sum > y.sum)) //sort based on sum revert
  }

  def i_dominates_j(a: Point, b: Point): Boolean = {
    a.values
      .zip(b.values) //combine the 2 values
      .count(x => x._1 > x._2) == 0 // count how many values of a are greater than b's
  }

  def skyline(dataPoints:RDD[Point]):RDD[Int]={
    dataPoints.cartesian(dataPoints) //create the cartesian product of data points with itself
      .filter(x => x._1.id != x._2.id) //remove the pairs that refer to the same id
      .map(x=>{
        (x._2.id, if(i_dominates_j(x._1,x._2)) 1 else 0)
      }) //0 if _2 is not getting dominated, 1 if it does
      .reduceByKey(_+_)
      .filter(_._2>0) //keep the nodes that are not dominated by any other node
      .map(_._1)
  }


  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf()
      .setMaster("local[16]") //The number of CPUs to use.
      .setAppName("Skyline")
    val spark = SparkSession.builder().config(sparkConf).getOrCreate()
    val sc = spark.sparkContext
    Logger.getLogger("org").setLevel(Level.OFF)


    var startTime = System.currentTimeMillis()
    val csvName_list: List[String] = List("datasets/norm_dimPoints_20_numPoints_10000.csv")
    for (csvName <- csvName_list) {
      println(csvName)
      // --- Task 1 --- //
      val dataPoints_list:RDD[Point] = readCsv(csvName)
      val skyline_list = skyline(dataPoints_list).collect()
      println("Skyline: ")
      skyline_list.foreach(x=> println(s"Point $x"))

      var finishTime = System.currentTimeMillis()
      print(finishTime - startTime)
      println("ms")
//       --- Task 2 --- //
      startTime = System.currentTimeMillis()
      val k = 10
      val dominatedPoints_sorted_list:RDD[(Point,Int)] = dataPoints_list
        .cartesian(dataPoints_list) //create the cartesian product of data points with itself
        .filter(x => x._1.id != x._2.id) //remove the pairs that refer to the same id
        .filter(a => i_dominates_j(a._1, a._2)) //keep only the pairs that the first one dominates the second one
        .map(x => (x._1, 1))
        .reduceByKey(_+_)
        .sortBy(_._2,ascending = false)

        dominatedPoints_sorted_list.persist(StorageLevel.MEMORY_AND_DISK)


      println(s"The top-$k points with the highest dominance score: ")
        dominatedPoints_sorted_list.take(k).foreach(x=>println(s"${x._1.id} with score ${x._2}")) //print them

      finishTime = System.currentTimeMillis()
      print(finishTime - startTime)
      println("ms")

      // --- Task 3 --- //
      startTime = System.currentTimeMillis()
      println(s"The top-$k points in the skyline with the highest dominance score: ")
      val bc = sc.broadcast(skyline_list)
      dominatedPoints_sorted_list
        .filter(x=>bc.value.contains(x._1.id)) //maintain only the points that belong to the skyline
        .take(k) //keep only the top k
        .foreach(x=>println(s"Point ${x._1.id} with score ${x._2}"))

      finishTime = System.currentTimeMillis()
      print(finishTime - startTime)
      println("ms")
    }
  }
}
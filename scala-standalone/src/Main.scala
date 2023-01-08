import scala.collection.mutable.ListBuffer
import scala.io.Source

object Main {
  case class Point(id: Int, values: List[Double], sum: Double)

  def readCsv(filename: String): List[Point] = {
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
    records.toList.sortWith((x, y) => x.sum > y.sum) //sort based on sum revert
  }

  def i_dominates_j(a: Point, b: Point): Boolean = {
    a.values
      .zip(b.values) //combine the 2 values
      .count(x => x._1 > x._2) == 0 // count how many values of a are greater than b's
  }

  def sieve_dataPoints(dataPoints_list: List[Point], ascOrder_flag: Boolean = true): List[Point] = {
    dataPoints_list
      .flatMap(x => dataPoints_list.map(y => (x, y))) //create the cartesian product of data points with itself
      .filter(x => x._1.id != x._2.id) //remove the pairs that refer to the same id
      .filter(a => i_dominates_j(a._1, a._2)) //keep only the pairs that the first one dominates the second one
      .map(_._1) //maintain the first point
      .distinct //remove duplicates
  }


  def main(args: Array[String]): Unit = {

    val csvName_list: List[String] = List("anti_dimPoints_20_numPoints_1000.csv")
    for (csvName <- csvName_list) {
      println(csvName)
      // --- Task 1 --- //
      val dataPoints_list = readCsv(csvName)
      var skyline_list = sieve_dataPoints(dataPoints_list)
      var finish = false
      while (!finish) {
        val temp_list = sieve_dataPoints(skyline_list)
        if (temp_list.nonEmpty) skyline_list = temp_list
        else finish=true
      }
      println("Skyline: ")
      skyline_list.map(_.id).foreach(x=> println(s"Point $x"))

      // --- Task 2 --- //
      val k = 10
      val dominatedPoints_sorted_list:List[(Point,Int)] = dataPoints_list
        .flatMap(x => dataPoints_list.map(y => (x, y))) //create the cartesian product of data points with itself
        .filter(x => x._1.id != x._2.id) //remove the pairs that refer to the same id
        .filter(a => i_dominates_j(a._1, a._2)) //keep only the pairs that the first one dominates the second one
        .map(x => (x._1, 1))
        .groupBy(_._1) // groups by the same point
        .map(x => (x._1, x._2.size)) //count how many times each record appears in the list
        .toList.sortWith((x,y)=>x._2>y._2) //sort based on the dominated points in desc order


      println(s"The top-$k points with the highest dominance score: ")
      dominatedPoints_sorted_list.take(k) //maintain the top k
        .foreach(x=>println(s"${x._1.id} with score ${x._2}")) //print them

      // --- Task 3 --- //
      println(s"The top-$k points in the skyline with the highest dominance score: ")
      val skyline_ids = skyline_list.map(_.id)
      dominatedPoints_sorted_list
        .filter(x=>skyline_ids.contains(x._1.id)) //maintain only the points that belong to the skyline
        .take(k) //keep only the top k
        .foreach(x=>println(s"Point ${x._1.id} with score ${x._2}"))
    }
  }
}
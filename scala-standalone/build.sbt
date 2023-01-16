
val sparkVersion = "3.0.0"

ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.17"
ThisBuild / name := "Skyline"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion, //% "provided",
  "org.apache.spark" %% "spark-sql" % sparkVersion)
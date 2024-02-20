package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

// LOAD CSV DATA INTO MAPS
func load_data(directory string) {

	People = make(map[int]people)
	Movies = make(map[int]movie)
	Names = make(map[string][]int)

	// Load data from CSV files into memory.
	// Load people
	file := fmt.Sprintf("%s/people.csv", directory)
	f, err := os.Open(file)
	if err != nil {
		log.Fatal(err)
	}
	// remember to close the file at the end of the program
	defer f.Close()

	// read csv values using csv.Reader
	csvReader := csv.NewReader(f)
	// Ignore header line in file
	header, _ := csvReader.Read()
	//fmt.Println(header)
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		m := make([]int, 0)
		key, _ := strconv.Atoi(record[0])
		p := people{record[1], record[2], m}
		People[key] = p
		Names[strings.ToLower(record[1])] = append(Names[strings.ToLower(record[1])], key)
	}

	// Load movies
	file = fmt.Sprintf("%s/movies.csv", directory)
	f2, err := os.Open(file)
	if err != nil {
		log.Fatal(err)
	}
	// remember to close the file at the end of the program
	defer f2.Close()

	// read csv values using csv.Reader
	csvReader = csv.NewReader(f2)
	header, _ = csvReader.Read()
	//fmt.Println(header)
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		m := make([]int, 0)
		key, _ := strconv.Atoi(record[0])
		a := movie{record[1], record[2], m}
		Movies[key] = a
	}

	// Load movies
	file = fmt.Sprintf("%s/stars.csv", directory)
	f3, err := os.Open(file)
	if err != nil {
		log.Fatal(err)
	}
	// remember to close the file at the end of the program
	defer f3.Close()

	// read csv values using csv.Reader
	csvReader = csv.NewReader(f3)
	header, _ = csvReader.Read()
	fmt.Println(header)
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		k1, _ := strconv.Atoi(record[0])
		k2, _ := strconv.Atoi(record[1])

		x := append(People[k1].movies, k2)
		y := append(Movies[k2].stars, k1)

		new_item1 := People[k1]
		new_item1.movies = x

		new_item2 := Movies[k2]
		new_item2.stars = y

		People[k1] = new_item1
		Movies[k2] = new_item2
	}
}

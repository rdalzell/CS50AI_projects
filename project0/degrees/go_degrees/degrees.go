package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type people struct {
	name   string
	birth  string
	movies []int
}

type movie struct {
	title string
	year  string
	stars []int
}

type movie_actor struct {
	movie_id int
	actor_id int
}

type node struct {
	actor_id int // Actor ID
	movie_id int // Movie ID
	parent   *node
}

var Frontier []*node

var Names map[string][]int
var People map[int]people
var Movies map[int]movie

// Return ID of named actor
func person_id_for_name(name string) int {
	/*
	   Returns the IMDB id for a person's name,
	   resolving ambiguities as needed.
	*/
	person_ids := Names[strings.ToLower(name)]

	if len(person_ids) == 0 {
		return 0
	} else if len(person_ids) > 1 {
		fmt.Println("MULTIPLE IDS FOUND")
		return 0
	} else {
		return person_ids[0]
	}

}

func in_frontier(f []*node, actor_id int) bool {
	for _, n := range f {
		if n.actor_id == actor_id {
			return true
		}
	}
	return false
}
func shortest_path(source int, target int) []movie_actor {

	/*
	   Returns the shortest list of (movie_id, person_id) pairs
	   that connect the source to the target.

	   If no possible path, returns None.
	*/

	num_explored := 0
	solution := make([]movie_actor, 0)

	// Create new node
	n := new(node)
	*n = node{source, 0, nil}

	Frontier = append(Frontier, n)
	Explored := make(map[int]bool)

	for {
		if len(Frontier) == 0 {
			return solution
		}

		// Get node from the front of the list (QUEUE)
		n = Frontier[0]
		Frontier = Frontier[1:]
		num_explored += 1

		if n.actor_id == target {
			fmt.Println("GOT A SOLUTION")
			for i := n; i.parent != nil; i = i.parent {
				//fmt.Println(i, *i.parent)
				solution = append(solution, movie_actor{i.movie_id, i.actor_id})
			}
			// Reverse the list
			for i, j := 0, len(solution)-1; i < j; i, j = i+1, j-1 {
				solution[i], solution[j] = solution[j], solution[i]
			}
			return solution

		}

		Explored[n.actor_id] = true

		// Add neighbors to frontier
		neighbors := neighbors_for_person(n.actor_id)

		for _, pair := range neighbors {
			// Have we explored this actor before?
			explored := Explored[pair.actor_id]
			if (!in_frontier(Frontier, pair.actor_id)) && !explored {
				//if not frontier.contains_state(state) and state not in explored:
				child := new(node)
				*child = node{pair.actor_id, pair.movie_id, n}
				Frontier = append(Frontier, child)
			}
		}

		//fmt.Println("FRONTIER SIZE", len(Frontier))

	}

}

func neighbors_for_person(person_id int) []movie_actor {
	/*
	   Returns (movie_id, person_id) pairs for people
	   who starred with a given person.
	*/

	movie_ids := People[person_id].movies
	neighbors := make([]movie_actor, 0)

	for _, movie_id := range movie_ids {
		for _, person_id := range Movies[movie_id].stars {
			pair := movie_actor{movie_id, person_id}
			neighbors = append(neighbors, pair)
		}
	}

	return neighbors
}

func main() {

	directory := os.Args[1:]
	load_data(directory[0])

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter source name: ")
	source_text, _ := reader.ReadString('\n')
	fmt.Print("Enter target name: ")
	target_text, _ := reader.ReadString('\n')

	source := person_id_for_name(source_text[:len(source_text)-1])
	target := person_id_for_name(target_text[:len(target_text)-1])

	if source == 0 {
		fmt.Printf("Can't find actor %s\n", source_text)
		os.Exit(0)
	}

	if target == 0 {
		fmt.Printf("Can't find actor %s\n", target_text)
		os.Exit(0)
	}

	path := shortest_path(source, target)

	if len(path) == 0 {
		fmt.Println("Not connected.")
	} else {
		degrees := len(path)
		fmt.Printf("%d degrees of separation.\n", degrees)
		header := movie_actor{0, source}
		path = append([]movie_actor{header}, path...)

		for i := 0; i < len(path)-1; i++ {
			person1 := People[path[i].actor_id].name
			person2 := People[path[i+1].actor_id].name
			movie := Movies[path[i+1].movie_id].title
			fmt.Printf("%d: %s and %s starred in %s\n", i+1, person1, person2, movie)
		}
	}
}

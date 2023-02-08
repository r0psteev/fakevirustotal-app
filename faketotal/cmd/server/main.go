package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"github.com/gorilla/mux"
	"github.com/r0psteev/faketotal/internal/malwarestore"
	inmem "github.com/r0psteev/faketotal/internal/malwarestore/store/memory"
	"io/ioutil"
	"log"
	"net/http"
)

var (
	store = inmem.NewInMemoryStore()
)

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/malware", addSample).Methods("POST")
	r.HandleFunc("/malware/{hash}", getSample).Methods("GET")
	log.Fatal(http.ListenAndServe(":8080", r))
}

func addSample(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	newSample := &malwarestore.MalwareSample{
		ID: uuid.New().String(),
	}

	// decode
	body, _ := ioutil.ReadAll(r.Body)
	log.Printf("Body: %s\n", body)
	err := json.Unmarshal(body, &newSample)
	if err != nil {
		panic(err)
	}

	newSample.ID = uuid.New().String()
	store.InsertSample(newSample)
	log.Printf("%v\n", newSample)
}

func getSample(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	// Get ID
	params := mux.Vars(r)
	hash := params["hash"]

	sample, err := store.FindSample(hash)
	if err != nil {
		panic(err)
	}
	// Return the foound sample
	json.NewEncoder(w).Encode(sample)
}

/*
func getSampleByHash(c *gin.Context) {
	hash := c.Param("hash")
}*/

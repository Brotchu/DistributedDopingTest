package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"sync"
)

var countries = []string{"ie", "gb", "de"}

// "ie"
// "gb"
// "de"

func main() {
	fmt.Println("starting registration testing")
	//get ip as cli argument
	ip := os.Args[1]

	//start worker pool
	wg := &sync.WaitGroup{}
	athleteChan := make(chan *RegistraionData)

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go registrationWorker(ip, athleteChan, wg)
	}

	//feed to channel for worker pool
	for id := 0; id < 10000; id++ {
		i := rand.Intn(len(countries))
		a := NewRegistrationData(fmt.Sprintf("load_test_user%d", id), countries[i], countries[i])
		athleteChan <- a
	}
	close(athleteChan)

	wg.Wait()

}

type RegistraionData struct {
	Name            string `json:"name"`
	Password        string `json:"password"`
	ConfirmPassword string `json:"confirm_password"`
	Email           string `json:"email"`
	Nationality     string `json:"nationality"`
	Location        string `json:"location"`
}

func NewRegistrationData(user, c, l string) *RegistraionData {
	return &RegistraionData{
		Name:            user,
		Password:        "password1",
		ConfirmPassword: "password1",
		Email:           user + "@gmail.com",
		Nationality:     c,
		Location:        l,
	}
}

func registrationWorker(ip string, inchan chan *RegistraionData, wg *sync.WaitGroup) {
	client := &http.Client{}
	for {
		athlete := <-inchan
		if athlete == nil {
			break
		}
		jsonData, err := json.Marshal(athlete)
		if err != nil {
			log.Panicln(err.Error())
		}
		// log.Println(string(jsonData))
		request, err := http.NewRequest("POST", ip, bytes.NewBuffer(jsonData))
		if err != nil {
			log.Panicln(err.Error())
		}
		request.Header.Set("Content-Type", "application/json; charset=UTF-8")

		resp, err := client.Do(request)
		if err != nil {
			log.Panicln(err.Error())
		}
		if resp.StatusCode != http.StatusOK {
			log.Panicln(resp.Status)
		}
		resp.Body.Close()
	}
	wg.Done()
}

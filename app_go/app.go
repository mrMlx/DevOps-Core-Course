package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"runtime"
	"strings"
	"time"
)

var startTime = time.Now()

type ServiceInfo struct {
	Name		string `json:"name"`
	Version		string `json:"version"`
	Description	string `json:"description"`
	Framework	string `json:"framework"`
}

type SystemInfo struct {
	Hostname 		string `json:"hostname"`
	Platform		string `json:"platform"`
	PlatformVersion	string `json:"platform_version"`
	Architecture	string `json:"architecture"`
	CPUCount		int 	`json:"spu_count"`
	PythonVersion 	string `json:"python_version"`
}

type RuntimeInfo struct {
	UptimeSeconds int    `json:"uptime_seconds"`
	UptimeHuman   string `json:"uptime_human"`
	CurrentTime   string `json:"current_time"`
	Timezone      string `json:"timezone"`
}

type RequestInfo struct {
	ClientIP  string `json:"client_ip"`
	UserAgent string `json:"user_agent"`
	Method    string `json:"method"`
	Path      string `json:"path"`
}

type Endpoint struct {
	Path        string `json:"path"`
	Method      string `json:"method"`
	Description string `json:"description"`
}

type RootResponse struct {
	Service   ServiceInfo   `json:"service"`
	System    SystemInfo    `json:"system"`
	Runtime   RuntimeInfo   `json:"runtime"`
	Request   RequestInfo   `json:"request"`
	Endpoints []Endpoint    `json:"endpoints"`
}

type HealthResponse struct {
	Status        string `json:"status"`
	Timestamp     string `json:"timestamp"`
	UptimeSeconds int    `json:"uptime_seconds"`
}


func getSystemInfo() SystemInfo {
	hostname, _ := os.Hostname()
	return SystemInfo{
		Hostname:        hostname,
		Platform:        runtime.GOOS,       // Аналог platform.system()
		PlatformVersion: runtime.GOARCH,     // Архитектура (amd64)
		Architecture:    runtime.GOARCH,
		CPUCount:        runtime.NumCPU(),   // Количество ядер
		PythonVersion:   runtime.Version(),  // Версия Go (ключ оставили python_version для совместимости)
	}
}

func getUptime() (int, string) {
	uptime := time.Since(startTime)
	secs := int(uptime.Seconds())
	human := fmt.Sprintf("%d hour, %d minutes", secs/3600, (secs%3600)/60)
	return secs, human
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	secs, _ := getUptime()
	data := HealthResponse{
		Status:        "ok",
		Timestamp:     time.Now().UTC().Format(time.RFC3339),
		UptimeSeconds: secs,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	secs, human := getUptime()
	
	// В Go IP-адрес клиента приходит вместе с портом (например, "127.0.0.1:54321").
	// Функция strings.Split отрезает порт по двоеточию и оставляет только IP.
	clientIP := strings.Split(r.RemoteAddr, ":")[0]

	data := RootResponse{
		Service: ServiceInfo{
			Name:        "my-devops-service",
			Version:     "1.0.0",
			Description: "Go application for DevOps lab",
			Framework:   "net/http",
		},
		System: getSystemInfo(),
		Runtime: RuntimeInfo{
			UptimeSeconds: secs,
			UptimeHuman:   human,
			CurrentTime:   time.Now().UTC().Format(time.RFC3339),
			Timezone:      "UTC",
		},
		Request: RequestInfo{
			ClientIP:  clientIP,
			UserAgent: r.UserAgent(),
			Method:    r.Method,
			Path:      r.URL.Path,
		},
		Endpoints: []Endpoint{
			{Path: "/", Method: "GET", Description: "Returns full service and system info"},
			{Path: "/health", Method: "GET", Description: "Health check endpoint"},
		},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/health", healthHandler)

	fmt.Println("Go server is running on port 5001...")
	http.ListenAndServe(":5001", nil)
}
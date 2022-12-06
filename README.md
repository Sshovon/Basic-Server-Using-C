# Network programming and administration of network services

### Milestone 1: Server Basic
- **Functional requirements**

1. Server written in C programming.
2. Server sends response with a specific type of file (as-is). The sample of asis file is given in the server-basic folder.
3. If there is an http request for a file that doesn't exist, or for a file of a type that is not supported, then the correct http error message must be returned to the client.
4. The server must be demonized.

- **Safety / robustness requirements**

1. The program should not bind to the gate once per. request, but only at program start.
2. Each client request must be processed in a separate thread or process.
3.  The server must be demonized so that it is independent of the control terminal.
4. The server it listens on port 80 without it running as the user root .
5. The directory that contains the files that should be accessible via http should be on web root.
6. Prevent zombie processes.


### Milestone 2: Server Custom

1.  Extend the server from milestone 1 so that it can deliver file types listed in /etc/mime.types. The identification of type must be done using the file extension.
2. The server should be running in a busybox-based container to be created using chroot and unshare so that access to files and processes is restricted.
3. Create a web page that has at least one image. The web page should be styled, using a CSS file.


### Milestone 3: RESTful API and WEB Interface
- **Functional requirements**

1. Two Docker containers must be made.
2. Create a Docker image that should be based on the official Docker image httpd:alpine and  set up so that the web server Apache supports the CGI standard.

3. Create a sqlite database: a poem storage.
4. Create a CGI program. CGI is mainly a shell  script which provides RESTful API against Sqlite database mentioned above.
5. In api the possible operations are, login, logout, if logged in- retrive a specific poem, retrieve all poems, add a new poem, delete own poem, update own poem, delete all own poems. 
6. XML must be used in request and response body. 
7. Create another CGI program, which runs in a seperate container to provide a WEB interface for the mentioned RESTful API.
8. RESTful API and WEB interface must run in seperate containers.


- **Safety / robustness requirements**

1. root the user in the container must be unprivileged in the host system using namespaces.
2. The processor use of the container must be limited using cgroups.
3. Security should be increased by capabilities



### Milestone 4: WEB Application using FETCH API
- **Functional requirements**

1. The client shall provide users with the same functionality as the CGI-based web interface from feature functional requirement 5. in Milestone 3.
2. The files that it consists of must be delivered by the C-based server from Milestone Milestone 1 And Milestone 2

3. When using a browser that supports Service workers , the client should set up a service worker that stores all the files it needs (HTML, js, css, etc.) and the
poems (HTTP responses) in a cache, so that the client's read operations can operate "offline".


### Project Architecture 
![This is an image](/Architecture.png)
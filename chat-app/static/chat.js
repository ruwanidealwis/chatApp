const socketIO = io.connect("http://" + document.domain + ":" + location.port);
console.log("hi");
socketIO.on("connect", () => {
  socketIO.emit("connected", {
    username: `${username}`,
  });

  onMessageSubmit = (event) => {
    event.preventDefault();
    socketIO.emit("message", {
      user_name: username,
      message: document.getElementById("message").value,
    });
  };
});
socketIO.on("my response", (msg) => {
  console.log(msg);
});

socketIO.on("new active user", (msg) => {
  console.log(msg.username);
  console.log("hi new active user");
  const newUser = document.createElement("li");
  newUser.appendChild(document.createTextNode(msg.username));
  document.getElementById("activeUsers").appendChild(newUser);
});

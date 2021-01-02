const socketIO = io.connect("http://" + document.domain + ":" + location.port);
sessionStorage.setItem("username", username);
/**
 * gets new message
 */

socketIO.on("connect", () => {
  console.log(socketIO);
  sessionStorage.setItem("socketID", socketIO.id);
  socketIO.emit("connected", {
    username: sessionStorage.getItem("username"),
    socketID: socketIO.id,
  });

  addGuest = (guestUsername) => {
    socketIO.emit("add to room", { userID: gu });
  };
  newPrivateMessage = (event) => {
    // random function from: https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
    const roomName = Math.random().toString(36).substring(7);
    console.log(event.currentTarget.value);
    console.log(sessionStorage.getItem("socketID"));
    console.log("creating room!");

    socketIO.emit("join room", {
      roomName: roomName,
      username: sessionStorage.getItem("username"), //own client's id
    });

    socketIO.emit("send invite", {
      roomName: roomName,
      userID: event.target.value,
    });
  };

  onMessageSubmit = (event) => {
    event.preventDefault();
    socketIO.emit("message", {
      username: username,
      message: document.getElementById("message").value,
      roomName: sessionStorage.getItem("currentRoom"),
    });
  };
});
//need to display message
socketIO.on("my response", (msg) => {
  let messageDiv = document.getElementById(msg.roomName);
  if (messageDiv === null) {
    messageDiv = document.createElement("div");
    messageDiv.id = msg.roomName;
  }
  const linebreak = document.createElement("br");
  messageDiv.appendChild(linebreak);
  const message = document.createTextNode(`${msg.username}: ${msg.message}`);
  messageDiv.appendChild(message);
  document.getElementById("chat-messages").appendChild(messageDiv);
});

socketIO.on("accept invite", (invite) => {
  socketIO.emit("join room", {
    roomName: invite.roomName,
    username: invite.username,
  });
});

socketIO.on("joined room", (data) => {
  console.log(data);
  sessionStorage.setItem("currentRoom", data.roomName);
});

socketIO.on("new active user", (msg) => {
  console.log(msg.username);
  console.log("hi new active user");

  //add new active user to list
  const newUser = document.createElement("li");
  const button = document.createElement("Button");

  //check if username is saved in session storage
  //TODO this works under the assumption that all usernames are unique, this is not enforced in the sign up page

  if (msg.username == sessionStorage.getItem("username"))
    button.appendChild(document.createTextNode(`${msg.username} (me)`));
  else button.appendChild(document.createTextNode(msg.username));

  newUser.appendChild(button);
  document.getElementById("activeUsers").appendChild(newUser);
  console.log(msg.socketID);
  button.value = msg.socketID;
  button.onclick = newPrivateMessage;
});

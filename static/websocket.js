const roomName = JSON.parse(document.getElementById("room-name").textContent);
const username = JSON.parse(document.getElementById("username").textContent);
// var username = {{ username }};
const chatSocket = new ReconnectingWebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onopen = function (e) {
  console.log("Connection Established");
  console.info("hello");
  fetchMessages(roomName);
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  if (data["command"] === "messages") {
    for (let i = 0; i < data["messages"].length; i++) {
      createMessage(data["messages"][i]);
    }
  } else if (data["command"] === "new_message") {
    createMessage(data["message"]);
  }else if (data["command"] === "update_likes") {
    update_likes();
  }
};

chatSocket.onclose = function (e) {
  console.info(e);
  console.error("Chat socket closed unexpectedly");
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  const messageInputDom = document.querySelector("#chat-message-input");
  const message = messageInputDom.value;
  console.log(message);
  console.log(username);
  chatSocket.send(
    JSON.stringify({
      message: message,
      command: "new_message",
      from: username,
      room: roomName,
    })
  );
  messageInputDom.value = "";
};

function fetchMessages(roomName) {
  console.info("hello2");
  console.log("fetch command sent");
  chatSocket.send(
    JSON.stringify({ command: "fetch_messages", room: roomName })
  );
}

function createMessage(message) {
  var author = message["author"];
  var msgListTag = document.createElement("li");
  var imgTag = document.createElement("img");
  var pTag = document.createElement("p");
  var p2Tag = document.createElement("p");
  var aTag = document.createElement("button");
  pTag.textContent = message.content;
  p2Tag.textContent = message.likes;
  aTag.onclick = function (e) {
    console.info("clicked");
    chatSocket.send(
      JSON.stringify({
        command: "like_message",
        room: roomName,
        liked_by: username,
        id: message.id,
      })
    );
  };
  aTag.className = "chat-customlike";
  aTag.textContent = "like";

  if (author == username) {
    msgListTag.className = "replies";
  } else {
    msgListTag.className = "sent";
  }
  msgListTag.appendChild(imgTag);
  msgListTag.appendChild(pTag);
  msgListTag.appendChild(p2Tag);
  p2Tag.appendChild(aTag);
  document.querySelector("#chat-log").appendChild(msgListTag);
  console.log("object created");
}
function update_likes() {
  var e = document.querySelector("#chat-log");
  console.log(e)
  //e.firstElementChild can be used.
  var child = e.lastElementChild; 
  while (child) {
      e.removeChild(child);
      child = e.lastElementChild;
  }
  fetchMessages(roomName)
}
const appChat = (roomName, messages, userId, userName) => {
  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
  );
  let userSet = new Set();

  // on message
  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.message_type !== 3) {
      $("#chat-log").append(
        $('<li class="card m-1 p-3 bg-white text-dark">').append(data.message)
      );
      $("#chat-log")
        .stop()
        .animate({ scrollTop: $("#chat-log")[0].scrollHeight }, 1000);
    }
    if (data.message_type === 2) {
      // delete user
      userSet.delete(data.user_name);
    } else {
      // ping or open socket
      console.log(data.user_name, ": ", data.message_type);
      userSet.add(data.user_name);
    }
    let str = "";
    userSet.forEach(function (user) {
      str +=
        '<div class="badge bg-warning text-dark text-wrap">' +
        user +
        "</div><br/>";
    });
    document.getElementById("active-users").innerHTML = str;
  };
  messages.forEach(function (item) {
    $("#chat-log").append(
      $('<li class="card m-1 p-3 bg-white text-dark">').append(item)
    );
  });
  $("#chat-log")
    .stop()
    .animate({ scrollTop: $("#chat-log")[0].scrollHeight }, 1000);

  // on close
  chatSocket.onclose = function (e) {
    console.log("Chat socket closed unexpectedly");
  };

  $(window).bind("beforeunload", function () {
    chatSocket.close();
  });

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
    chatSocket.send(
      JSON.stringify({
        user_id: userId,
        message_type: 0,
        message: userName + ": " + message,
      })
    );
    messageInputDom.value = "";
  };

  // on open
  chatSocket.onopen = function (e) {
    console.log("connection is open!");
    chatSocket.send(
      JSON.stringify({
        user_id: userId,
        message_type: 1,
        message: userName + " has joined the chat",
      })
    );
    setInterval(() => {
      chatSocket.send(
        JSON.stringify({
          user_id: userId,
          message_type: 3,
          message: "",
        })
      );
    }, 2000);
  };
};

onUsernameSubmit = async (event) => {
  event.preventDefault();

  const username = document.getElementById("username").value;

  //send request
  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    body: JSON.stringify({ username: username }),
  }).then((response) => {
    if (response.ok) {
      console.log("good");
      location.replace(response.url);
    } else {
      console.error("something went wrong when entering username");
    }
  });

  console.log();
};

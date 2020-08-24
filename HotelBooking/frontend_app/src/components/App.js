import React, { Component } from "react";
import ReactDom from "react-dom";

class App extends Component {
  render() {
    try {
      // there are 2 ways to query 'user' variable from request, but we have to declare them first in index.html
      var id = JSON.parse(document.querySelector("#id").textContent);
      var username = document.querySelector("#username").dataset.user;

      console.log(id);
      console.log(username);
    } catch (error) {
      username = "";
    }
    return (
      <div>
        <h1 className="text-primary bg-dark">
          Ay {id} {username}
        </h1>
      </div>
    );
  }
}

ReactDom.render(<App />, document.getElementById("app"));

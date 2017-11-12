import React from "react";
import ReactDOM from "react-dom";
import AppLayout from "./AppLayout";
import injectTapEventPlugin from "react-tap-event-plugin";

injectTapEventPlugin();

ReactDOM.render(<AppLayout/>, document.getElementById('app-layout'));
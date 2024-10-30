import React from "react";
import PacketTable  from "./components/PacketTable";
import "./sniffer.css";

function sniffer(){
  return (
    <div className="sniffer">
      <h1>Мониторинг сетевого трафика</h1>
      <PacketTable />
    </div>
  );
}

export default sniffer;
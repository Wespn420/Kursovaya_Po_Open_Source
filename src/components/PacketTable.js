import React, { useEffect, useState } from "react";
import axios from "axios";

const PacketTable = () => {
    const [packets, setPackets] = useState([]);

    const fetchPackets = async () => {
        try {
            const responce = await axios.get("http://127.0.0.1:5000/packets");
            setPackets(responce.data);
        } catch (error){
            console.error("Ошибка при получении пакетов:", error);
        }
    };

    useEffect (() => {
        fetchPackets();
        const interval = setInterval(fetchPackets, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
          <h2>Захваченные пакеты</h2>
          <table>
            <thead>
              <tr>
                <th>Протокол</th>
                <th>Источник IP</th>
                <th>Назначение IP</th>
                <th>Источник Порт</th>
                <th>Назначение Порт</th>
              </tr>
            </thead>
            <tbody>
              {packets.map((packet, index) => (
                <tr key={index}>
                  <td>{packet.protocol_name}</td>
                  <td>{packet.src_ip}</td>
                  <td>{packet.dst_ip}</td>
                  <td>{packet.src_port || "N/A"}</td>
                  <td>{packet.dst_port || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );      
};

export default PacketTable;
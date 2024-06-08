import { Image } from "@chakra-ui/react";
import React from "react";
import { useSelector } from "react-redux";
import { Form, Message } from "../../components";
import { StateType } from "../../types";
import styles from "./Main.module.css";
interface Props {}
const Main: React.FC<Props> = ({}) => {
  const messages = useSelector(({ messages }: StateType) => messages);
  return (
    <div className={styles.main}>
      <div className={styles.main__header}>
        <Image src="/logo.jpeg" alt="main-logo" />
        <h1>The AI Therapist</h1>
        <p></p>
      </div>
      <div className={styles.main__main}>
        {messages.length === 0 ? (
          <p>
            Introducing <strong>Your Therapist Friend </strong>, a digital tool designed to assist with therapeutic conversations.

          </p>
        ) : (
          messages.map((message, index) => (
            <Message key={index} message={message} />
          ))
        )}
      </div>
      <Form />
    </div>
  );
};

export default Main;

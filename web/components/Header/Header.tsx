import { Image } from "@chakra-ui/react";
import React from "react";
import styles from "./Header.module.css";
interface Props {}
const Header: React.FC<Props> = ({}) => {
  return (
    <div className={styles.header}>
      <Image src = "https://drive.google.com/thumbnail?id=1V2viL2AoK-7dpHTw8z4t_sA9n34mJ6n7" alt="main-logo" />
      
    </div>
  );
};

export default Header;

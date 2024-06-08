import React from 'react';
import styles from "./Footer.module.css";
interface Props {}
const  Footer: React.FC<Props> = ({}) => {
    return (
       <p className={styles.footer}>
        Made By - Byte System
       </p>
    );
};

export default  Footer;
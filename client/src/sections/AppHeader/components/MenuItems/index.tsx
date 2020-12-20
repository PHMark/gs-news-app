import React from "react";
import { Link } from "react-router-dom";
import { useApolloClient } from "@apollo/react-hooks";
import { Avatar, Button, Menu } from "antd";
import { PlusSquareOutlined, LogoutOutlined, UserOutlined }  from "@ant-design/icons";
import { LOG_OUT } from "../../../../lib/graphql/queries";
import { userLogout, userLogoutVariables } from "../../../../lib/graphql/queries/Logout/__generated__/userLogout";
import { displaySuccessNotification, displayErrorMessage } from "../../../../lib/utils";
import { Viewer } from "../../../../lib/types";

interface Props {
  viewer: Viewer;
  setViewer: (viewer: Viewer) => void;
}

const { Item, SubMenu } = Menu;

export const MenuItems = ({ viewer, setViewer }: Props) => {
  const client = useApolloClient();
  const handleLogOut = async () => {
    try {
      await client.query<userLogout, userLogoutVariables>({
        query: LOG_OUT,
        variables: { token: viewer.user_login }
      });
      setViewer({ user_login: null });
      displaySuccessNotification("You've successfully logged out!");
    } catch {
      displayErrorMessage(
        "Sorry! We weren't able to log you out. Please try again later!"
      );
    }
  };

  const subMenuLogin =
    viewer.user_login ? (
      <SubMenu title={<Avatar src={"https://www.gravatar.com/avatar"} />}>
        <Item key="/user">
          <Link to={`/user/${viewer.user_login}`}>
            <UserOutlined translate="" />
              Profile
          </Link>
        </Item>
        <Item key="/logout">
          <div onClick={() => handleLogOut()}>
            <LogoutOutlined translate="" />
            Log out
          </div>
        </Item>
      </SubMenu>
    ) : (
      <Item>
        <Link to="/login">
          <Button type="primary">Sign In</Button>
        </Link>
      </Item>
    );

  return (
    <Menu mode="horizontal" selectable={false} className="menu">
      <Item key="/create">
        <Link to="/create">
          <PlusSquareOutlined translate="" />
          New Topic
        </Link>
      </Item>
      {subMenuLogin}
    </Menu>
  );
};

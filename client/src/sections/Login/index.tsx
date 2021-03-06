import React, { useState } from "react";
import jwtDecode, { JwtPayload } from "jwt-decode";
import { Redirect } from "react-router";
import { useMutation } from "@apollo/react-hooks";
import { Form, Input, Button, Card, Layout, Spin, Typography } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import {
  userLogin,
  userLoginVariables,
} from "../../lib/graphql/mutations/Login/__generated__/userLogin";
import {
  ERROR_LOG_IN_DENIED,
  ERROR_MESSAGE,
} from "../../lib/promptMessages/error";
import { SUCCESS_LOGIN } from "../../lib/promptMessages/success";
import { ErrorBanner } from "../../lib/components";
import { LOG_IN } from "../../lib/graphql/mutations";
import { displaySuccessNotification } from "../../lib/utils";
import { Viewer } from "../../lib/types";

interface Props {
  setViewer: (user_login: Viewer) => void;
  viewer: Viewer;
}

interface JwtProps extends JwtPayload {
  identity: string;
  user_claims: string;
}

const { Content } = Layout;
const { Text, Title } = Typography;

export const Login = ({ viewer, setViewer }: Props) => {
  const [errorMsg, setErrorMsg] = useState(ERROR_MESSAGE);
  const [logIn, { loading: logInLoading, error: logInError }] = useMutation<
    userLogin,
    userLoginVariables
  >(LOG_IN, {
    onCompleted: (data) => {
      if (data && data.user_login && data.user_login.token) {
        const decoded = jwtDecode<JwtProps>(data.user_login.token);
        setViewer({
          token: data.user_login.token,
          id: decoded.identity,
          avatar: decoded.user_claims,
        });
        localStorage.setItem("token", data.user_login.token);
        localStorage.setItem("id", decoded.identity);
        localStorage.setItem("avatar", decoded.user_claims);
        displaySuccessNotification(SUCCESS_LOGIN);
      }
    },
    onError: (data) => {
      const gqlErrors = data.graphQLErrors && data.graphQLErrors?.length ? data.graphQLErrors[0] : null;
      if (gqlErrors) {
        const errorMessage = gqlErrors.message;
        setErrorMsg(errorMessage);
      }
    },
  });

  const handleLogin = async (login: userLoginVariables) => {
    logIn({ variables: login });
  };

  if (logInLoading) {
    return (
      <Content className="log-in">
        <Spin size="large" tip="Logging you in..." />
      </Content>
    );
  }

  if (viewer.id || viewer.token) {
    const { id: userId } = viewer;
    return <Redirect to={`/user/${userId}`} />;
  }

  const logInErrorBannerElement = logInError ? (
    <ErrorBanner description={errorMsg} message={ERROR_LOG_IN_DENIED} />
  ) : null;

  return (
    <Content className="log-in">
      {logInErrorBannerElement}
      <Card className="log-in-card">
        <div className="log-in-card-intro">
          <Title level={3} className="log-in-card__intro-title">
            <span role="img" aria-label="wave">
              👋
            </span>
          </Title>
          <Title level={3} className="log-in-card__intro-title">
            Log in to GS News!
          </Title>
          <Text>Sign in to start getting news updates about Growsari!</Text>
        </div>
        <Form
          name="normal_login"
          className="log-in-form"
          onFinish={handleLogin}
        >
          <Form.Item
            name="email"
            rules={[{ required: true, message: "Please input your Email!" }]}
          >
            <Input
              prefix={
                <UserOutlined translate="" className="site-form-item-icon" />
              }
              placeholder="Email"
            />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: "Please input your Password!" }]}
          >
            <Input
              prefix={
                <LockOutlined translate="" className="site-form-item-icon" />
              }
              type="password"
              placeholder="Password"
            />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="log-in-form-button"
            >
              Sign in
            </Button>
          </Form.Item>
          <Form.Item>
            <Text>
              Or <a href="/register">register now!</a>
            </Text>
          </Form.Item>
        </Form>
      </Card>
    </Content>
  );
};

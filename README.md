# Workshop cho AWS
> AWS là một dịch vụ cloud computing của Amazon

> AWS Amplify là một Javascript framework giúp sử dụng các dịch vụ AWS dễ dàng hơn

## Bắt đầu

```bash
npm install -g @aws-amplify/cli
amplify configure
```
- Specify the AWS Region: 
- Specify the username of the new IAM user: __amplify-workshop-user__
> Trong AWS Console, chọn __Next: Permissions__, __Next: Tags__, __Next: Review__, & __Create User__ để tạo một IAM user mới. Sau đó, trở lại command line và nhấn Enter.
- Enter the access key of the newly created user:   
  accessKeyId: __(<YOUR_ACCESS_KEY_ID>)__   
  secretAccessKey:  __(<YOUR_SECRET_ACCESS_KEY>)__
- Profile Name: __amplify-workshop-user__

```bash
amplify init
```
- Enter a name for the project: __amplifyreactapp__
- Enter a name for the environment: __dev__
- Choose your default editor: __Visual Studio Code (or your default editor)__   
- Please choose the type of app that you're building __javascript__   
- What javascript framework are you using __react__   
- Source Directory Path: __src__   
- Distribution Directory Path: __build__   
- Build Command: __npm run-script build__   
- Start Command: __npm run-script start__   
- Do you want to use an AWS profile? __Y__
- Please choose the profile you want to use: __amplify-workshop-user__

## Mô tả sản phẩm
- Cho phép người dùng đăng nhập
- Tạo database để lưu trữ thông tin album, photo
- Thêm và chỉnh sửa album, thêm và chỉnh sửa ảnh trong từng album
- Dán nhãn cho từng photo

## Đăng nhập và bảo mật (AWS Cognito)
### Backend
```bash
amplify add auth
```

- Do you want to use the default authentication and security configuration? __Default configuration__
- How do you want users to be able to sign in? __Username__
- Do you want to configure advanced settings? __No, I am done.__

> `amplify add` dùng để thêm service của AWS vào app. `Auth` là dịch vụ để dăng kí, đăng nhập, quản lý người dùng và xác minh người dùng của AWS.

```bash
amplify push
```
- Are you sure you want to continue? __Yes__

> Lệnh này để thêm những gì vừa làm vào server của AWS. Sau khi thêm service __Auth__, trong [AWS Console Management](https://console.aws.amazon.com) chọn Cognito > Manage User Pool sẽ thấy User Pool vùa tạo

### Frontend
> Cần phải có một giao diện để người dùng có thể đăng nhập

```bash
npm install --save aws-amplify aws-amplify-react
```

> Thêm vào __src/index.js__. Những dòng code dưới sẽ liên kết AWS vào app. Vì vậy phải thêm vào __src/index.js__ để đảm bảo toàn bộ app đều có thể dùng AWS.
```js
import Amplify from 'aws-amplify'
import config from './aws-exports'
Amplify.configure(config)
```

> Thêm vào __src/App.js__ thư viện `aws-amplify-react`. Đó là một thư viện có chứa một số React Component của AWS để giúp việc kết nối tới AWS được dễ dàng hơn. Higher Order Component `withAuthenticator` sẽ cung cấp một màn hình đăng nhập với đầy đủ chức năng
```js
import { withAuthenticator } from 'aws-amplify-react'
```

> Gói Component `App` lại bằng Component `withAuthenticator` để màn hình đăng nhập hoạt động. Sửa dòng `export default App` 
```js
export default withAuthenticator(App, { includeGreetings: true })
```

## API để quản lý album
> Trên AWS, tạo ra một table để quản lý tên và thông tin về album. Cần có một API để lấy và gửi thông tin từ server. [GraphQL API](https://graphql.org/learn/) sẽ được sử dụng.

### Backend (AWS Appsync)
```bash
amplify add api
```

- Please select from one of the below mentioned services: __GraphQL__
- Provide API name: __photoalbums__ (Tên mà các bạn muốn)
- Choose an authorization type for the API: __Amazon Cognito User Pool__
- Do you have an annotated GraphQL schema: __No__
- Do you want a guided schema creation: __Yes__
- What best describes your project: __One-to-many relationship (e.g., “Blogs” with “Posts” and “Comments”)__
- Do you want to edit the schema now: __Yes__
- Please manually edit the file created at
- Do you want to configure advanced settings for the GraphQL API: __No, I am done.__

> Chỉnh sửa __amplify/backend/api/(<Tên_API>)/schema.graphql__ thành:
```graphql
type Album @model @auth(rules: [{allow: owner}]) {
    id: ID!
    name: String!
    photos: [Photo] @connection(name: "AlbumPhotos")
}

type Photo @model @auth(rules: [{allow: owner}]) {
    id: ID!
    album: Album @connection(name: "AlbumPhotos")
    bucket: String!
    fullsize: PhotoS3Info!
    thumbnail: PhotoS3Info!
}

type PhotoS3Info {
    key: String!
    width: Int!
    height: Int!
}
```

> `@auth(rules: [{allow: owner}])` sẽ cho phép duy nhất người tạo album được xem album

### Thử tạo album bằng AWS Console Management
```
amplify console api > GraphQL
```
![GraphQL Queries Screen](GraphQL.png)
> Để thực hiện Query, các bạn phải login bằng một user mà các bạn đã tạo ở phần Authentication. ClienID nằm trong __src/aws-exports.js__ phần __aws_user_pools_web_client_id__. Thử tạo một album tên First Album bằng dòng Query dưới đây
```graphql
mutation {
    createAlbum(input:{name:"First Album"}) {
        id
        name
    }
}
```
> Thêm một album mới tên Second Album
```graphql
mutation {
    createAlbum(input:{name:"Second Album"}) {
        id
        name
    }
}
```
> Hiện tất cả các album
```graphql
query {
    listAlbums {
        items {
            id
            name
        }
    }
}
```

### Frontend
```bash
npm install --save react-router-dom semantic-ui-react
```
> Semantic-ui-react thư viện UI cho React, react-router-dom thư viện để navigation giữa các trang với nhau trong React. Thêm dòng dưới vào giữa tag __head__ trong __public/index.html__
```html
<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.3.3/semantic.min.css"></link>
```
> Sửa __src/App.js__ thành
```js
import React, { Component } from 'react';

import { Grid, Header, Input, List, Segment } from 'semantic-ui-react';
import {BrowserRouter as Router, Route, NavLink} from 'react-router-dom';

import Amplify, { API, graphqlOperation } from 'aws-amplify';
import { Connect, withAuthenticator } from 'aws-amplify-react';

import aws_exports from './aws-exports';
Amplify.configure(aws_exports);

function makeComparator(key, order='asc') {
  return (a, b) => {
    if(!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) return 0; 

    const aVal = (typeof a[key] === 'string') ? a[key].toUpperCase() : a[key];
    const bVal = (typeof b[key] === 'string') ? b[key].toUpperCase() : b[key];

    let comparison = 0;
    if (aVal > bVal) comparison = 1;
    if (aVal < bVal) comparison = -1;

    return order === 'desc' ? (comparison * -1) : comparison
  };
}


const ListAlbums = `query ListAlbums {
    listAlbums(limit: 9999) {
        items {
            id
            name
        }
    }
}`;

const SubscribeToNewAlbums = `
  subscription OnCreateAlbum {
    onCreateAlbum {
      id
      name
    }
  }
`;


const GetAlbum = `query GetAlbum($id: ID!) {
  getAlbum(id: $id) {
    id
    name
  }
}
`;


class NewAlbum extends Component {
  constructor(props) {
    super(props);
    this.state = {
      albumName: ''
      };
    }

  handleChange = (event) => {
    let change = {};
    change[event.target.name] = event.target.value;
    this.setState(change);
  }

  handleSubmit = async (event) => {
    event.preventDefault();
    const NewAlbum = `mutation NewAlbum($name: String!) {
      createAlbum(input: {name: $name}) {
        id
        name
      }
    }`;
    
    const result = await API.graphql(graphqlOperation(NewAlbum, { name: this.state.albumName }));
    console.info(`Created album with id ${result.data.createAlbum.id}`);
    this.setState({ albumName: '' })
  }

  render() {
    return (
      <Segment>
        <Header as='h3'>Add a new album</Header>
          <Input
          type='text'
          placeholder='New Album Name'
          icon='plus'
          iconPosition='left'
          action={{ content: 'Create', onClick: this.handleSubmit }}
          name='albumName'
          value={this.state.albumName}
          onChange={this.handleChange}
          />
        </Segment>
      )
    }
}


class AlbumsList extends React.Component {
  albumItems() {
    return this.props.albums.sort(makeComparator('name')).map(album =>
      <List.Item key={album.id}>
        <NavLink to={`/albums/${album.id}`}>{album.name}</NavLink>
      </List.Item>
    );
  }

  render() {
    return (
      <Segment>
        <Header as='h3'>My Albums</Header>
        <List divided relaxed>
          {this.albumItems()}
        </List>
      </Segment>
    );
  }
}


class AlbumDetailsLoader extends React.Component {
  render() {
    return (
      <Connect query={graphqlOperation(GetAlbum, { id: this.props.id })}>
        {({ data, loading }) => {
          if (loading) { return <div>Loading...</div>; }
          if (!data.getAlbum) return;

          return <AlbumDetails album={data.getAlbum} />;
        }}
      </Connect>
    );
  }
}


class AlbumDetails extends Component {
  render() {
    return (
      <Segment>
        <Header as='h3'>{this.props.album.name}</Header>
        <p>TODO: Allow photo uploads</p>
        <p>TODO: Show photos for this album</p>
      </Segment>
    )
  }
}


class AlbumsListLoader extends React.Component {
    onNewAlbum = (prevQuery, newData) => {
        // When we get data about a new album, we need to put in into an object 
        // with the same shape as the original query results, but with the new data added as well
        let updatedQuery = Object.assign({}, prevQuery);
        updatedQuery.listAlbums.items = prevQuery.listAlbums.items.concat([newData.onCreateAlbum]);
        return updatedQuery;
    }

    render() {
        return (
            <Connect 
                query={graphqlOperation(ListAlbums)}
                subscription={graphqlOperation(SubscribeToNewAlbums)} 
                onSubscriptionMsg={this.onNewAlbum}
            >
                {({ data, loading }) => {
                    if (loading) { return <div>Loading...</div>; }
                    if (!data.listAlbums) return;

                return <AlbumsList albums={data.listAlbums.items} />;
                }}
            </Connect>
        );
    }
}


class App extends Component {
  render() {
    return (
      <Router>
        <Grid padded>
          <Grid.Column>
            <Route path="/" exact component={NewAlbum}/>
            <Route path="/" exact component={AlbumsListLoader}/>

            <Route
              path="/albums/:albumId"
              render={ () => <div><NavLink to='/'>Back to Albums list</NavLink></div> }
            />
            <Route
              path="/albums/:albumId"
              render={ props => <AlbumDetailsLoader id={props.match.params.albumId}/> }
            />
          </Grid.Column>
        </Grid>
      </Router>
    );
  }
}

export default withAuthenticator(App, {includeGreetings: true});
```
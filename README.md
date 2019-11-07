# Workshop cho AWS
> AWS là một dịch vụ cloud computing của Amazon

> AWS Amplify là một Javascript framework giúp sử dụng các dịch vụ AWS dễ dàng hơn

## Bắt đầu

```
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

`
amplify init
`
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
`
amplify add auth
`

- Do you want to use the default authentication and security configuration? __Defau
lt configuration__
- How do you want users to be able to sign in? __Username__
- Do you want to configure advanced settings? __No, I am done.__

> `amplify add` dùng để thêm service của AWS vào app. `Auth` là dịch vụ để dăng kí, đăng nhập, quản lý người dùng và xác minh người dùng của AWS.

`
amplify push
`
- Are you sure you want to continue? __Yes__

> Lệnh này để thêm những gì vừa làm vào server của AWS. Sau khi thêm service __Auth__, trong [AWS Console Management](https://console.aws.amazon.com) chọn Cognito > Manage User Pool sẽ thấy User Pool vùa tạo

### Frontend
> Cần phải có một giao diện để người dùng có thể đăng nhập

`
npm install --save aws-amplify aws-amplify-react
`

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

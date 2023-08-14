# GitLab Management from the console

Many GitLab Management tasks can be achieved via the console on the GitLab sever.  Via two different supplied tools ```gitlab-rake``` and ```gitlab-rails```, both tools need to be run on the GitLab server so initially the administrator will need to connect to the GitLab server.

## Connecting via SSH to GitLab server

To Connect to the GitLab server via SSH:

1. Open a command prompt or terminal
2. Login into the GitLab server using SSH

    ```bash
    ssh admin@gitlab.localhost.com
    ```

3. Enter the user password
4. The prompt should now change to a bash prompt  

    ```bash
    admin@gitlab.localhost.com:~$
    ```

5. Once finished close the SSH session by typing ```exit```, ```logout```, ```Ctrl```+```D```, or ```~.```

## Connecting to a GitLab docker server

To Connect to the GitLab docker server:

1. Open a command prompt or terminal
2. Login into the GitLab server using SSH

    ``` bash
    docker exec -it gitlab gitlab-rails console
    ```

3. The prompt should now change to  

    ``` bash
    irb(main):001:0>
    ```

## Creating a user

To create a user account:

1. SSH into your GitLab server.
2. Start a Ruby on Rails console:

    ```bash
    sudo gitlab-rails console -e production
    ```

3. Create the user  

    ```ruby
    u = User.new(username: 'test_user', email: 'test@example.com', name: 'Test User', password: 'password', password_confirmation: 'password')
    ```

4. Disable user confirmation as no email servers exist  

    ```ruby
    u.skip_confirmation! 
    ```

5. Save the changes  

    ```ruby
    u.save!
    ```

6. Exit the console with ```Control```+```d```

## Changing passwords

To change a user account password:

1. SSH into your GitLab server.
2. Start a Ruby on Rails console:

    ```bash
    sudo gitlab-rails console -e production
    ```

3. In the console you can then, find a user

    ```ruby
    user = User.find_by_username 'exampleuser'
    ```

4. Then change the password:

    ```ruby
    new_password = 'examplepassword'
    user.password = new_password
    user.password_confirmation = new_password
    ```

5. Exit the console with ```Control```+```d```

Alternatively you can also change the password using gitlab-rake:

1. SSH into your GitLab server.
2. Change the user password

    ```bash
    sudo gitlab-rake "gitlab:password:reset[uname]"
    ```

## Unlock a user

To unlock a locked user:

1. SSH into your GitLab server.
2. Start a Ruby on Rails console:

    ```bash
    sudo gitlab-rails console -e production
    ```

3. Find the user to unlock. You can search by email or ID.

    ```ruby
    user = User.find_by(email: 'admin@local.host')
    ```

    or

    ```ruby
    user = User.where(id: 1).first
    ```

4. Unlock the user:

    ```ruby
    user.unlock_access!
    ```

5. Exit the console with ```Control```+```d```

## Adding Users to Groups/Projects

To add all users to a group/project:

1. SSH into your GitLab server.
2. Add all users:

    ```bash
    sudo gitlab-rake gitlab:import:all_users_to_all_groups
    ```

    or

    ```bash
    sudo gitlab-rake gitlab:import:all_users_to_all_projects
    ```

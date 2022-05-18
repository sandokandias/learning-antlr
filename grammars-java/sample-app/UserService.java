public class UserService {

    public UserService(){
    }

    public void save(User user) {
        System.out.println("Saving user " + user);
    }

    public void cancel(String username) {
        System.out.println("Cancelling user " + username);
    }
}
const UserDetail = ({ user }) => {
    return (
        <div className="user-display-format">
            <p><strong>Name:</strong> {user.user_name}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Public API Key:</strong> {user.api_key_public}</p>
            <p><strong>Private API Key:</strong> {user.api_key_private}</p>
            <p><strong>Base URL:</strong> {user.base_url}</p>
        </div>
    );
}

export default UserDetail;
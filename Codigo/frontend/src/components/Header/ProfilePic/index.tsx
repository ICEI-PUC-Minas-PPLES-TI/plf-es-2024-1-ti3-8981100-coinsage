import DefaultProfilePic from '/profile.svg'

interface ProfilePicProps {
    size?: number;
}

const ProfilePic: React.FC<ProfilePicProps> = ({ size }) => {
    return (
        <img style={{
            width: size ? `${size}px` : '50px',
            height: size ? `${size}px` : '50px',
            borderRadius: '50%',
            cursor: 'pointer',
        }} src={DefaultProfilePic} alt="Profile"/>
    );
}

export default ProfilePic;

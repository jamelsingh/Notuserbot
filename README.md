import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, SkipForward, SkipBack, Volume2, Heart, Search, Music, Home, Library, User } from 'lucide-react';

const TamilSongsApp = () => {
  const [currentSong, setCurrentSong] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.7);
  const [activeTab, setActiveTab] = useState('home');
  const [favorites, setFavorites] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  
  const audioRef = useRef(null);

  // Sample Tamil songs data (in real app, these would be actual audio files)
  const songs = [
    {
      id: 1,
      title: "Ennodu Nee Irundhal",
      artist: "A.R. Rahman",
      album: "I (2015)",
      duration: "4:32",
      cover: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=300&fit=crop",
      audioUrl: "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav" // Demo audio
    },
    {
      id: 2,
      title: "Kadhal Rojave",
      artist: "A.R. Rahman",
      album: "Roja (1992)",
      duration: "5:15",
      cover: "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=300&h=300&fit=crop",
      audioUrl: "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
    },
    {
      id: 3,
      title: "Munbe Vaa",
      artist: "A.R. Rahman",
      album: "Sillunu Oru Kaadhal (2006)",
      duration: "4:45",
      cover: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop",
      audioUrl: "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
    },
    {
      id: 4,
      title: "Vennilave Vennilave",
      artist: "A.R. Rahman",
      album: "Minsara Kanavu (1997)",
      duration: "6:12",
      cover: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=300&fit=crop",
      audioUrl: "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
    },
    {
      id: 5,
      title: "Yaaradi Nee Mohini",
      artist: "Dhanush",
      album: "Yaaradi Nee Mohini (2008)",
      duration: "4:28",
      cover: "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=300&h=300&fit=crop",
      audioUrl: "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
    }
  ];

  const filteredSongs = songs.filter(song => 
    song.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    song.artist.toLowerCase().includes(searchQuery.toLowerCase()) ||
    song.album.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleNext);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleNext);
    };
  }, [currentSong]);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleNext = () => {
    setCurrentSong((prev) => (prev + 1) % songs.length);
    setIsPlaying(true);
  };

  const handlePrev = () => {
    setCurrentSong((prev) => (prev - 1 + songs.length) % songs.length);
    setIsPlaying(true);
  };

  const handleSeek = (e) => {
    const audio = audioRef.current;
    const clickX = e.nativeEvent.offsetX;
    const width = e.target.offsetWidth;
    const newTime = (clickX / width) * duration;
    audio.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleVolumeChange = (e) => {
    const newVolume = e.target.value;
    setVolume(newVolume);
    audioRef.current.volume = newVolume;
  };

  const toggleFavorite = (songId) => {
    setFavorites(prev => 
      prev.includes(songId) 
        ? prev.filter(id => id !== songId)
        : [...prev, songId]
    );
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const playSong = (index) => {
    setCurrentSong(index);
    setIsPlaying(true);
  };

  const NavBar = () => (
    <nav className="flex justify-around items-center py-4 bg-gradient-to-r from-red-600 to-orange-500 text-white">
      <button 
        onClick={() => setActiveTab('home')}
        className={`flex flex-col items-center ${activeTab === 'home' ? 'text-yellow-300' : ''}`}
      >
        <Home size={24} />
        <span className="text-xs mt-1">Home</span>
      </button>
      <button 
        onClick={() => setActiveTab('search')}
        className={`flex flex-col items-center ${activeTab === 'search' ? 'text-yellow-300' : ''}`}
      >
        <Search size={24} />
        <span className="text-xs mt-1">Search</span>
      </button>
      <button 
        onClick={() => setActiveTab('library')}
        className={`flex flex-col items-center ${activeTab === 'library' ? 'text-yellow-300' : ''}`}
      >
        <Library size={24} />
        <span className="text-xs mt-1">Library</span>
      </button>
      <button 
        onClick={() => setActiveTab('profile')}
        className={`flex flex-col items-center ${activeTab === 'profile' ? 'text-yellow-300' : ''}`}
      >
        <User size={24} />
        <span className="text-xs mt-1">Profile</span>
      </button>
    </nav>
  );

  const SongList = ({ songs, title }) => (
    <div className="p-4">
      <h2 className="text-xl font-bold text-gray-800 mb-4">{title}</h2>
      <div className="space-y-3">
        {songs.map((song, index) => (
          <div 
            key={song.id}
            className={`flex items-center p-3 rounded-lg cursor-pointer transition-all duration-200 ${
              currentSong === songs.indexOf(song) ? 'bg-red-100 border-l-4 border-red-500' : 'bg-white hover:bg-gray-50'
            } shadow-sm`}
            onClick={() => playSong(songs.indexOf(song))}
          >
            <img 
              src={song.cover} 
              alt={song.title}
              className="w-12 h-12 rounded-lg object-cover mr-3"
            />
            <div className="flex-grow">
              <h3 className="font-semibold text-gray-800 text-sm">{song.title}</h3>
              <p className="text-gray-600 text-xs">{song.artist} • {song.album}</p>
            </div>
            <div className="flex items-center space-x-2">
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  toggleFavorite(song.id);
                }}
                className={`p-1 ${favorites.includes(song.id) ? 'text-red-500' : 'text-gray-400'}`}
              >
                <Heart size={18} fill={favorites.includes(song.id) ? 'currentColor' : 'none'} />
              </button>
              <span className="text-xs text-gray-500">{song.duration}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const HomeTab = () => (
    <div className="flex-1 overflow-y-auto bg-gradient-to-b from-orange-50 to-white">
      <div className="p-4">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">வணக்கம்! Welcome</h1>
        <p className="text-gray-600 mb-6">Discover the best of Tamil music</p>
        
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">Featured Playlist</h2>
          <div className="bg-gradient-to-r from-red-500 to-orange-500 rounded-lg p-4 text-white">
            <h3 className="text-xl font-bold mb-1">A.R. Rahman Hits</h3>
            <p className="text-orange-100 text-sm mb-3">The maestro's timeless classics</p>
            <button className="bg-white text-red-600 px-4 py-2 rounded-full text-sm font-semibold">
              Play Now
            </button>
          </div>
        </div>
      </div>
      
      <SongList songs={songs} title="Trending Tamil Songs" />
    </div>
  );

  const SearchTab = () => (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="p-4">
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search songs, artists, albums..."
            className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-red-500"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
      
      {searchQuery ? (
        <SongList songs={filteredSongs} title="Search Results" />
      ) : (
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Popular Searches</h2>
          <div className="grid grid-cols-2 gap-3">
            {['A.R. Rahman', 'Ilaiyaraaja', 'Harris Jayaraj', 'Yuvan Shankar Raja'].map(artist => (
              <button 
                key={artist}
                className="bg-white p-4 rounded-lg shadow-sm text-left hover:bg-gray-50"
                onClick={() => setSearchQuery(artist)}
              >
                <Music className="text-red-500 mb-2" size={24} />
                <p className="font-semibold text-gray-800">{artist}</p>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const LibraryTab = () => {
    const favoriteSongs = songs.filter(song => favorites.includes(song.id));
    
    return (
      <div className="flex-1 overflow-y-auto bg-gray-50">
        <SongList songs={favoriteSongs} title="Your Favorites ❤️" />
        
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recently Played</h2>
          <div className="space-y-2">
            {songs.slice(0, 3).map(song => (
              <div key={song.id} className="flex items-center p-2 bg-white rounded-lg">
                <img src={song.cover} alt={song.title} className="w-10 h-10 rounded mr-3" />
                <div>
                  <p className="font-semibold text-sm text-gray-800">{song.title}</p>
                  <p className="text-xs text-gray-600">{song.artist}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const ProfileTab = () => (
    <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
      <div className="bg-white rounded-lg p-6 mb-4 text-center">
        <div className="w-20 h-20 bg-gradient-to-r from-red-500 to-orange-500 rounded-full mx-auto mb-4 flex items-center justify-center">
          <User size={32} className="text-white" />
        </div>
        <h2 className="text-xl font-bold text-gray-800">Music Lover</h2>
        <p className="text-gray-600">Tamil Music Enthusiast</p>
      </div>
      
      <div className="bg-white rounded-lg p-4">
        <h3 className="font-semibold text-gray-800 mb-3">Stats</h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Songs Played</span>
            <span className="font-semibold">1,247</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Favorites</span>
            <span className="font-semibold">{favorites.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Hours Listened</span>
            <span className="font-semibold">156h</span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex flex-col h-screen bg-gray-100 max-w-md mx-auto">
      {/* Header */}
      <header className="bg-gradient-to-r from-red-600 to-orange-500 text-white p-4">
        <h1 className="text-2xl font-bold text-center">🎵 Tamil Songs</h1>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'home' && <HomeTab />}
        {activeTab === 'search' && <SearchTab />}
        {activeTab === 'library' && <LibraryTab />}
        {activeTab === 'profile' && <ProfileTab />}
      </div>

      {/* Now Playing Bar */}
      {songs[currentSong] && (
        <div className="bg-white border-t p-3">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center flex-1 min-w-0">
              <img 
                src={songs[currentSong].cover} 
                alt={songs[currentSong].title}
                className="w-10 h-10 rounded mr-3"
              />
              <div className="min-w-0 flex-1">
                <h4 className="font-semibold text-sm text-gray-800 truncate">{songs[currentSong].title}</h4>
                <p className="text-xs text-gray-600 truncate">{songs[currentSong].artist}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button onClick={handlePrev} className="text-gray-600 hover:text-red-500">
                <SkipBack size={20} />
              </button>
              <button 
                onClick={togglePlay}
                className="bg-red-500 text-white p-2 rounded-full hover:bg-red-600"
              >
                {isPlaying ? <Pause size={20} /> : <Play size={20} />}
              </button>
              <button onClick={handleNext} className="text-gray-600 hover:text-red-500">
                <SkipForward size={20} />
              </button>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="flex items-center space-x-2 text-xs text-gray-500">
            <span>{formatTime(currentTime)}</span>
            <div 
              className="flex-1 bg-gray-200 rounded-full h-1 cursor-pointer"
              onClick={handleSeek}
            >
              <div 
                className="bg-red-500 h-1 rounded-full"
                style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
              ></div>
            </div>
            <span>{formatTime(duration)}</span>
            <Volume2 size={16} className="text-gray-400" />
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={volume}
              onChange={handleVolumeChange}
              className="w-16 h-1"
            />
          </div>
        </div>
      )}

      {/* Navigation */}
      <NavBar />

      {/* Audio Element */}
      <audio
        ref={audioRef}
        src={songs[currentSong]?.audioUrl}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
      />
    </div>
  );
};

export default TamilSongsApp;

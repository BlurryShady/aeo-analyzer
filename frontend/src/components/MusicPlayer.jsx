import { useState, useRef, useEffect } from 'react'
import './MusicPlayer.css'

const playlist = [
  { name: "Dream Big", artist: "Onoychenko", src: "/music/Onoychenko-Dream-big.mp3" },
  { name: "Gospel of Bullets", artist: "Lappy", src: "/music/Lappy-The-gospel-of-bullets.mp3" },
  { name: "The Grey Room", artist: "Nebula", src: "/music/Nebula-The-grey-room-density-and-time.mp3" },
  { name: "Japanese Lofi", artist: "Torii", src: "/music/Torii-Japanese-lofi.mp3" }
]



function MusicPlayer() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isExpanded, setIsExpanded] = useState(false)
  const [volume, setVolume] = useState(1)
  const audioRef = useRef(null)
  const [hasShone, setHasShone] = useState(false)


  useEffect(() => {
  if (audioRef.current) {
    audioRef.current.load()
    if (isPlaying) audioRef.current.play()
  }
  }, [currentIndex])

  useEffect(() => {
  if (audioRef.current) {
    audioRef.current.volume = volume
  }
  }, [volume])

  useEffect(() => {
  const timer = setTimeout(() => setHasShone(true), 4500)
  return () => clearTimeout(timer)
  }, [])


  const togglePlay = () => {
  if (isPlaying) {
    audioRef.current.pause()
  } else {
    audioRef.current.play()
  }
  setIsPlaying(!isPlaying)
  }

  const nextTrack = () => {
  setCurrentIndex((currentIndex + 1) % playlist.length)
  }

  const prevTrack = () => {
  setCurrentIndex((currentIndex - 1 + playlist.length) % playlist.length)
  }

  const handleEnded = () => {
  nextTrack()
  }

  return (
    <div className={`music-player-container ${isExpanded ? 'expanded' : 'collapsed'} ${!hasShone ? 'shine' : ''}`}>
    <audio
        ref={audioRef}
        src={playlist[currentIndex].src}
        onEnded={handleEnded}
    />
    
    <div className="player-collapsed" onClick={() => setIsExpanded(!isExpanded)}>
        <span className="player-note">♪</span>
        <span className="player-title">{playlist[currentIndex].name}</span>
        <span className="player-artist">{playlist[currentIndex].artist}</span>
    </div>

    {isExpanded && (
        <div className="player-expanded" onClick={e => e.stopPropagation()}>
        <div className="player-controls">
            <button onClick={prevTrack}>⏮</button>
            <button onClick={togglePlay}>{isPlaying ? '⏸' : '▶'}</button>
            <button onClick={nextTrack}>⏭</button>
        </div>
        <div className="player-volume">
            <span>Vol</span>
            <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={volume}
            onChange={e => setVolume(parseFloat(e.target.value))}
            />
        </div>
        <div className="playlist">
            {playlist.map((track, i) => (
            <div
                key={i}
                className={`playlist-item ${i === currentIndex ? 'active' : ''}`}
                onClick={() => { setCurrentIndex(i); setIsPlaying(true) }}
            >
                <span>{track.name}</span>
                <span>{track.artist}</span>
            </div>
            ))}
        </div>
        </div>
    )}
    </div>
  )
}

export default MusicPlayer
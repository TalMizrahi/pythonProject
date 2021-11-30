var sounds = [
  'http://soundboard.panictank.net/2SAD4ME.mp3',
  'http://soundboard.panictank.net/AIRHORN.mp3',
  'http://soundboard.panictank.net/Darude - Dankstorm.mp3',
  'http://soundboard.panictank.net/HITMARKER.mp3',
  'http://soundboard.panictank.net/MOM GET THE CAMERA.mp3',
  'http://soundboard.panictank.net/Oh Baby A Triple.mp3',
  'http://soundboard.panictank.net/OMG TRICKSHOT CHILD.mp3',
  'http://soundboard.panictank.net/OOOOOOOOHMYGOOOOD.mp3',
  'http://soundboard.panictank.net/SANIC.mp3',
  'http://soundboard.panictank.net/SKRILLEX Scary.mp3',
  'http://soundboard.panictank.net/SMOKE WEEK EVERYDAY.mp3',
  'http://soundboard.panictank.net/WOMBO COMBO.mp3',
  'http://soundboard.panictank.net/DAMN SON WHERED YOU FIND THIS.mp3',
  'http://soundboard.panictank.net/Whatcha Say.mp3',
  'http://soundboard.panictank.net/2SED4AIRHORN.mp3',
  'http://soundboard.panictank.net/tactical nuke.mp3',
  'http://soundboard.panictank.net/intervention 420.mp3',
  'http://soundboard.panictank.net/AIRPORN.mp3',
  'http://soundboard.panictank.net/DEDOTADED WAM.mp3',
  'http://soundboard.panictank.net/DAMN SON WOW.mp3',
  'http://soundboard.panictank.net/GET NOSCOPED.mp3',
  'http://soundboard.panictank.net/AIRHORN SONATA.mp3',
  'http://soundboard.panictank.net/wow ;).mp3',
  'http://soundboard.panictank.net/SHOTS FIRED.mp3',
  'http://soundboard.panictank.net/NEVER DONE THAT.mp3',
  'http://soundboard.panictank.net/SPOOKY.mp3'
]

function yeah() {
  var sound = sounds[Math.floor(Math.random()*sounds.length)];
  var audio = new Audio(sound);
  audio.play();
}
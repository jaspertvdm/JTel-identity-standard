# WebRTC Signaling Hook (concept)

Doel: intent/continuity check op offer/answer/ICE voordat peers doorgaan.

## Flow
1) Signaling-server ontvangt event (offer/answer/ice-candidate) met session_id/peer info.
2) Stuurt naar router `/fira/init` bij sessie-start (initiatior/responder = peers, rol: webrtc_peer).
3) Voor elk signaling event: `/ift` met intent `"webrtc_offer"` of `"webrtc_answer"` of `"webrtc_ice"`; context = peer ids, sdp type, candidate info; continuity_hash_prev verplicht.
4) Bij 409/401 → flag/NIR; bij ok → relay naar peer.

## Minimal pseudo-code (Node/TS-ish)
```js
async function handleOffer({sessionId, from, to, sdp, prevHash}) {
  // ensure FIR/A exists
  if (!state[sessionId]) {
    const init = await post('/fira/init', {
      initiator: from, responder: to, roles: ['webrtc_peer'], context: {session: sessionId}
    });
    state[sessionId] = {fir_a_id: init.fir_a_id, hash: init.continuity_hash};
  }
  const {fir_a_id, hash} = state[sessionId];
  const resp = await post('/ift', {
    fir_a_id,
    intent: 'webrtc_offer',
    context: {from, to, session: sessionId, sdpType: 'offer'},
    continuity_hash_prev: prevHash || hash,
  });
  state[sessionId].hash = resp.continuity_hash;
  relayToPeer(to, {type:'offer', sdp});
}
```

## Richtlijnen
- Bewaar per sessie: fir_a_id + laatste continuity_hash.
- Gebruik JWT/mTLS tussen signaling-server en router.
- Whitelist intents: webrtc_offer, webrtc_answer, webrtc_ice.
- Rate-limit per peer/session; NIR/flag op mismatch.

## Uitbreiding
- Logging/audit van signaling events in Postgres (aan routerkant).
- Integratie in bestaande signaling server (Node/Python/Go) als middleware/interceptor.

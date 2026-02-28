"use client";

import { useState } from "react";

interface Props {
  headlines: string[];
  eventId: string;
}

export default function NewsSection({ headlines, eventId }: Props) {
  const [newsImgLoaded, setNewsImgLoaded] = useState(false);

  if (!headlines || headlines.length === 0) return null;

  return (
    <div className="news-section">
      <h3>Era Context</h3>
      {newsImgLoaded && (
        <div className="image-container">
          <img src={`/images/${eventId}/news.png`} alt="Era context" />
        </div>
      )}
      <img
        src={`/images/${eventId}/news.png`}
        alt=""
        style={{ display: "none" }}
        onLoad={() => setNewsImgLoaded(true)}
        onError={() => setNewsImgLoaded(false)}
      />
      <ul className="news-list">
        {headlines.map((h, i) => (
          <li key={i}>{h}</li>
        ))}
      </ul>
    </div>
  );
}

// 🚨 Palabras sospechosas estilo phishing
const phishingKeywords = [
  "urgent", "password", "confirm account", "click here",
  "reset your password", "bank", "security alert",
  "payment required", "account suspended"
];

export const detectPhishingText = (text) => {
  const found = phishingKeywords.filter(word =>
    text.toLowerCase().includes(word)
  );
  return found;
};

export const detectMaliciousContent = (text) => {
  let matches = [];

  const regexList = [
    /<script.*?>/gi,
    /SELECT .* FROM/gi,
    /DROP TABLE/gi,
    /--/g
  ];

  regexList.forEach((r) => {
    if (r.test(text)) matches.push(r.toString());
  });

  return matches;
};

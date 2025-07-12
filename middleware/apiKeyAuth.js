import dotenv from 'dotenv';
dotenv.config();

export const apiKeyAuth = (req, res, next) => {
  const clientKey = req.header('x-api-key');
  console.log('Gelen API Key:', clientKey); // DEBUG

  if (!clientKey || clientKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Geçersiz veya eksik API anahtarı' });
  }

  next();
};

/*
  # Create predictions table

  1. New Tables
    - `predictions`
      - `id` (uuid, primary key)
      - `disease` (text) - Name of the predicted disease
      - `confidence` (numeric) - Confidence percentage of the prediction
      - `language` (text) - Language selected for the health tip
      - `created_at` (timestamptz) - Timestamp of when the prediction was made

  2. Security
    - Enable RLS on `predictions` table
    - Add policy for public insert access (anyone can log predictions)
    - Add policy for public read access (anyone can view predictions)

  Note: For a production application, you would want to add user authentication 
  and restrict access to only the user's own predictions.
*/

CREATE TABLE IF NOT EXISTS predictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  disease text NOT NULL,
  confidence numeric NOT NULL,
  language text NOT NULL DEFAULT 'English',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access"
  ON predictions
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow public insert access"
  ON predictions
  FOR INSERT
  TO public
  WITH CHECK (true);

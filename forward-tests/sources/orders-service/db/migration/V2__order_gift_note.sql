ALTER TABLE orders ADD COLUMN gift_note text NULL CHECK (char_length(gift_note) <= 200);

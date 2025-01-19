-----
-- Return PC if available and valid, append woonplaats if available
----
CREATE OR REPLACE FUNCTION format_pc_wpl(postcode_in text, woonplaats_in text)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    adres varchar;
	pc 	varchar;
BEGIN
    -- Remove space between numbers and letters
    IF postcode_in ~ '^[1-9][0-9]{3}\s[A-Z]{2}$' THEN
        pc := REPLACE(postcode_in, ' ', '');
	ELSE
		pc := postcode_in;
    END IF;
	-- Check if postcode is valid format (e.g. 1234AB)
    IF pc ~ '^[1-9][0-9]{3}[A-Z]{2}$' THEN
        adres := pc;
    ELSE
        adres := '';
    END IF;
    IF woonplaats_in IS NOT NULL THEN
        adres := adres || ' ' || trim(woonplaats_in);
    END IF;
    RETURN trim(adres);
END;
$function$;
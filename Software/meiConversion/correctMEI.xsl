
<?xml-model href="https://music-encoding.org/schema/4.0.1/mei-CMN.rng"?> 
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="@* | node()">
         <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template> 
    
    <xsl:template match="*:beam"> <!-- remove double items in case of tuple beams -->
        <xsl:variable name="xmlItems" select="./@xml:id"/>
        <xsl:if test="count(//*:beam[@xml:id=$xmlItems])>1"> <!-- if xml:id occurs more than 1 time, delete -->
            <xsl:choose>
                <xsl:when test="parent::*:tuplet">
                     <xsl:copy-of select="."/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:if>     
    </xsl:template> 
    
    <xsl:template match="*:rest/*:verse"/> <!-- delete rests with verses -->
    
    <xsl:template match="*:title/*:title"> <!-- if titles are nested only use first one  -->
        <xsl:value-of select="."/>
    </xsl:template> 
</xsl:stylesheet>
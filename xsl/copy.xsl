<xsl:stylesheet
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        version="1.0" xmlns:t="http://www.tei-c.org/ns/1.0">

    <xsl:template match="node()|text()|@*">
        <xsl:copy>
            <xsl:apply-templates select="@*" />
            <xsl:apply-templates select="node()|text()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
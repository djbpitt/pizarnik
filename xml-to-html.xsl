<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xml" indent="yes" doctype-system="about:legacy-compat"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>Pizarnik collation demo</title>
                <link rel="stylesheet" href="http://www.obdurodon.org/css/style.css" type="text/css"
                />
            </head>
            <body>
                <h1>Pizarnik collation demo</h1>
                <table>
                    <xsl:apply-templates select="root/table"/>
                </table>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="table">
        <!-- collation sets -->
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="table/item">
        <!-- witness within a collation set -->
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>
    <xsl:template match="t">
        <xsl:apply-templates/>
        <xsl:text> </xsl:text>
    </xsl:template>
    <xsl:template match="add">
        <ins>
            <xsl:apply-templates/>
        </ins>
    </xsl:template>
    <xsl:template match="del">
        <del>
            <xsl:apply-templates/>
        </del>
    </xsl:template>
    <xsl:template match="gap">
        <span class="gap">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
</xsl:stylesheet>

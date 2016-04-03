<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:djb="http://www.obdurodon.org" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs" version="2.0">
    <xsl:strip-space elements="table"/>
    <xsl:output method="xml" indent="yes" doctype-system="about:legacy-compat"/>
    <xsl:function name="djb:titleCase" as="xs:string">
        <xsl:param name="input"/>
        <xsl:variable name="initial" select="substring($input, 1, 1)" as="xs:string"/>
        <xsl:variable name="remainder" select="substring($input, 2)" as="xs:string"/>
        <xsl:sequence select="concat(upper-case($initial), $remainder)"/>
    </xsl:function>
    <xsl:template match="/">
        <html>
            <head>
                <title>Pizarnik collation demo</title>
                <link rel="stylesheet" href="http://www.obdurodon.org/css/style.css" type="text/css"/>
                <style type="text/css">
                    th,
                    td{
                        border: none;
                    }
                    th{
                        text-align: left;
                        border-right: 1px solid gray;
                    }
                    ins{
                        text-decoration: none;
                        color: green;
                    }
                    del{
                        color: red;
                    }</style>
            </head>
            <body>
                <h1>Pizarnik collation demo</h1>
                <xsl:apply-templates select="root/table"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="table">
        <!-- collation sets -->
        <h2>
            <xsl:text>Line </xsl:text>
            <xsl:value-of select="position()"/>
        </h2>
        <table>
            <xsl:apply-templates/>
        </table>
    </xsl:template>
    <xsl:template match="table/item">
        <!-- witness within a collation set -->
        <xsl:variable name="position" select="position()" as="xs:integer"/>
        <tr>
            <th>
                <xsl:value-of
                    select="djb:titleCase(../following-sibling::witnesses[1]/item[$position])"/>
            </th>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>
    <xsl:template match="item/item">
        <!-- cells within a collation set -->
        <td>
            <xsl:apply-templates select="descendant::t"/>
        </td>
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
